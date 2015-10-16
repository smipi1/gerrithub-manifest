#!/bin/sh
#
# Copyright 2015 Philips Lighting
#
# Supplies helper functions to push updated files to git arhives
#
# NOTE: A function named error() must be defined to source this file:
#       It is assumed that error() prints all arguments to stderr

# Determines the svn relative URL of a directory under svn revision control
getSvnRelativeUrl() {
	local DIRECTORY=$1;shift
	if ! cd ${DIRECTORY}; then
		error "cannot cd to directory: ${DIRECTORY}"
		return 1
	elif ! svn info; then
		error "cannot get svn info: ${DIRECTORY}"
		return 1
	fi | if ! awk -F ':' '/^Relative URL/{print $2}'; then
		error "missing 'Relative URL' field: ${DIRECTORY}"
		return 1
	fi
	return 0
}

# Determines the Hue release number given a specified directory which is under svn revision control
getRelease() {
	local DIRECTORY=$1;shift
	if ! cd ${DIRECTORY}; then
		error "cannot cd to directory: ${DIRECTORY}"
		return 1
	elif ! svn info; then
		error "cannot get svn info: ${DIRECTORY}"
		return 1
	fi | if ! awk -F ':' '/^Revision/{printf ("01%06d\n", $2)}'; then
		error "missing 'Revision' field: ${DIRECTORY}"
		return 1
	fi
	return 0
}

# Converts an Philips Hue svn relative URL to a git branch name
# '^/Products/SmartBridge/trunk' or '^/Products/SmartBridge/Software' is converted to 'master'
# For everything else, '^/Products/SmartBridge/trunk' or '^/Products/SmartBridge/Software' is just stripped from the front
svnRelativeUrlToGitBranchName() {
	local RELATIVE_URL=$1;shift
	local PROJECT_ROOT=$1
	local SMARTBRIDGE_PATH=`echo ${RELATIVE_URL} | sed 's#\^/Products/SmartBridge/##g;s#/Software$##g'`
	case ${SMARTBRIDGE_PATH} in
	trunk)
		echo "master"
		;;
	branches/*)
		echo ${SMARTBRIDGE_PATH#*/}
		;;
	*)
		error "unsupported path determining git branch name: ${SMARTBRIDGE_PATH}"
		;;
	esac
}

# Converts a Philips Hue svn versioned directory to a branch name
getVersionedDirectoryBranchName() {
	local DIRECTORY=$1;shift
	local RELATIVE_URL="`getSvnRelativeUrl ${DIRECTORY}`"
	if [ "$?" -ne "0" ]; then
		error "cannot determine svn relative URL: ${DIRECTORY}"
		return 1
	elif ! svnRelativeUrlToGitBranchName ${RELATIVE_URL}; then
		error "cannot determine git branch name: ${RELATIVE_URL}"
		return 1
	else
		return 0
	fi
}

# Sets up an empty git workspace consistent with the specified svn source directory:
# The specified remote repository is added as an 'origin' remote
# A branchname is calculated from the svn source directory
# If the branch already exists on 'origin', a tracking branch is added
# If the branch doesn't yet exist, a new branch created
# No files are checked out, but HEAD is set up to point to the new/existing branch
setupEmptyGitWorkspaceForSvnSrcDir() {
	local SRC_DIR=$1;shift
	local DEST_DIR=$1;shift
	local DEST_REPO=$1;shift
	local GIT_BRANCH_NAME=`getVersionedDirectoryBranchName ${SRC_DIR}`
	if [ "$?" -ne "0" ]; then
		error "cannot determine git branch name: ${SRC_DIR}"
		return 1
	elif ! git init -q ${DEST_DIR}; then
		error "cannot initialize git workspace: ${DEST_DIR}"
		return 1
	elif ! cd ${DEST_DIR}; then
		error "cannot cd to git workspace: ${DEST_DIR}"
		return 1
	elif ! git remote add origin ${DEST_REPO}; then
		error "cannot add remote repository as origin: ${DEST_REPO}"
		return 1
	fi
	if ! git ls-remote -q origin; then
		error "cannot reach origin repository: ${DEST_REPO}"
		return 1
	fi | if ! grep -q ''refs/heads/${GIT_BRANCH_NAME}''; then
		# Branch doesn't yet exist on origin:
		# No need to fetch, just create and checkout locally
		if [ "${GIT_BRANCH_NAME}" = "master" ]; then
			# Already on master due to 'git init'
			return 0
		elif ! git checkout -q -b ${GIT_BRANCH_NAME}; then
			error "cannot create branch: ${GIT_BRANCH_NAME}"
			return 1
		else
			return 0
		fi
	elif ! git fetch --depth 1 -q origin ${GIT_BRANCH_NAME} 2>/dev/null; then
		error "cannot fetch branch from origin: ${GIT_BRANCH_NAME}"
		return 1
	elif ! git branch -q ${GIT_BRANCH_NAME} --track origin/${GIT_BRANCH_NAME}; then
		error "cannot create branch: ${GIT_BRANCH_NAME}"
		return 1
	elif ! git symbolic-ref HEAD refs/heads/${GIT_BRANCH_NAME}; then
		error "cannot reset the head to: ${GIT_BRANCH_NAME}"
		return 1
	else
		return 0
	fi
}

removeLeadingAndTrailingEmptyLines() {
	sed -e :a -e '/./,$!d;/^\n*$/{$d;N;};/\n$/ba'
	return $?
}

moveSvnCommitInfoToEnd() {
	local COMMIT_INFO
	local EMPTY_LINE
	if ! read COMMIT_INFO; then
		error "cannot read commit info"
		return 1
	elif ! read EMPTY_LINE; then
		error "cannot read empty line"
		return 1
	elif [ -n "${EMPTY_LINE}" ]; then
		error "commit info not followed by empty line"
		return 1
	elif ! removeLeadingAndTrailingEmptyLines; then
		error "cannot print commit message content"
		return 1
	else
		echo
		echo "${COMMIT_INFO}"
	fi
}

reformatSvnMessage() {
	if ! egrep -v "^-+$"; then
		error "cannot remove separators from commit message"
		return 1
	fi | if ! moveSvnCommitInfoToEnd; then
		error "cannot move commit info to the end of the message"
		return 1
	else
		return 0
	fi
}

# Generates and copies a git-formatted commit message from the svn history of the specified directory
copyVersionedCommitMessage() {
	local DIRECTORY=$1;shift
	local DEST=$1;shift
	if ! cd ${DIRECTORY}; then
		error "cannot cd to directory: ${DIRECTORY}"
		return 1
	elif ! svn log -l 1; then
		error "cannot get svn log: ${DIRECTORY}"
		return 1
	fi | if ! reformatSvnMessage; then
		error "cannot reformat svn log message: ${DIRECTORY}"
		return 1
	fi >${DEST} 
	return 0
}

originHasTag() {
	local TAG=$1
	if ! git ls-remote -q --tags origin; then
		error "cannot reach origin repository: ${DEST_REPO}"
		return 1
	fi | if grep -q ''refs/tags/${TAG}''; then
		return 0
	else
		return 1
	fi
}

# Commits all changes to a git workspace, tags the commit and pushes it to 'origin' 
commitTagAndPushAllFiles() {
	local DIRECTORY=$1;shift
	local COMMIT_MESSAGE_FILE=$1;shift
	local TAG=$1;shift
	if ! cd ${DIRECTORY}; then
		error "cannot cd to directory: ${DIRECTORY}"
		return 1
	elif ! git add -A >/dev/null; then
		error "cannot add all files: ${DIRECTORY}"
		return 1
	elif git diff-index -q HEAD -- 2>/dev/null; then
		echo "nothing to commit and push: no changes: ${DIRECTORY}"
		return 0
	elif originHasTag ${TAG}; then
		error "tag already exists at origin: ${TAG}"
		return 1
	elif ! git commit -F ${COMMIT_MESSAGE_FILE}; then
		error "cannot commit changes: ${DIRECTORY}"
		return 1
	elif ! git push origin HEAD; then
		error "cannot push HEAD to origin: ${DIRECTORY}"
		return 1
	elif ! git tag ${TAG}; then
		error "cannot tag HEAD: ${TAG}"
		return 1
	elif ! git push origin --tags; then
		error "cannot push tags to origin: ${DIRECTORY}"
		return 1
	else
		return 0
	fi
}
