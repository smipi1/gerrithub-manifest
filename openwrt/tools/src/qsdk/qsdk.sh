#!/bin/bash
#set -x

SELF=$0
QSDK_TOOLS_DIR=`dirname $(readlink -e $0)`
TOOLS_DIR=`readlink -e ${QSDK_TOOLS_DIR}/../..`
OPENWRT_DIR=`readlink -e ${TOOLS_DIR}/..`
QUALCOMM_DIR=${OPENWRT_DIR}/qualcomm
QSDK_DIR=${QUALCOMM_DIR}/qsdk
QSDK_SRC=${OPENWRT_DIR}/qsdkSource.mk
REPO_NAME=github
RED=31
YELLOW=33

printInColor() {
	local COLOR=$1;shift
	echo -n -e "\033[${COLOR}m${*}\033[0m\n"
}

echoRed() {
	printInColor ${RED} "$*" >&2
}

echoYellow() {
	printInColor ${YELLOW} "$*" >&2
}

warning() {
	echoRed "warning: $*" >&2
}

error() {
	echoRed "error: $*" >&2
}

abort() {
	error "$*"
	exit 1
}

showHelp() {
	local p
	echo "${SELF}: QSDK maintenance tool"
	echo
	echo "Usage: ${SELF} COMMAND [ARGS]"
	echo
	echo "COMMAND can be any of"
	echo "	fetch                  Fetches the latest for all QSDK repo projects"
	echo "	status                 Determines the status of all QSDK repo projects"
	echo "	start BRANCH           Starts a work BRANCH in all QSDK repo projects"
	echo "	push BRANCH            Pushes the work BRANCH to all QSDK github repositories"
	echo "	push BRANCH --delete   Deletes the work BRANCH from all QSDK github repositories"
	echo "	branch                 Shows branch information for all QSDK repo projects"
	echo "	stash                  Stashes the current branch for all QSKD repo projects for later use"
	echo "	                       Leaves all QSDK repo projects in detached HEAD state"
	echo "	                       Useful if you want to:"
	echo "	                       1. Prevent incoming changes to qsdkSource.mk from causing a merge"
	echo "	                          in the QSDK because you are still on a branch."
	echo "	                       2. Keep a branch to later continue work on (E.g. when termporarily"
	echo "	                          checking out an old version of the ipbridge build)."
	echo "	checkout BRANCH        Checks out a stashed or pushed branch for all QSDK repo projects"
	echo "	abandon BRANCH         Abandons (deletes) the work BRANCH in all QSDK repo projects"
	echo "	rebase MANIFEST        Rebase current qsdk state onto a specified (new) MANIFEST:"
	echo "	                       1. Checks that all QSDK repo projects are on the same branch"
	echo "	                       2. Initializes the QSDK repository with MANIFEST"
	echo "	                       3. Syncs the QSDK repository to start the rebase"
	echo "	ls-commits             Lists all committed MANIFESTS in the order that they were created."
	echo "	commit MANIFEST        Commit the current qsdk state under MANIFEST:"
	echo "	                       1. Checks that all QSDK repo projects are on the same branch and that there"
	echo "	                          are no uncommitted changes"
	echo "	                       2. Tags and pushes all QSDK repo projects with MANIFEST"
	echo "	                       3. Creates and pushes a MANIFEST.xml to the manifests repository"
	echo "	                          NOTE: You will have to enter a commit message"
	echo "	                       4. Updates `basename ${QSDK_SRC}` to point to MANIFEST.xml"
	echo "	                          NOTE: It is up to you to commit the change to `basename ${QSDK_SRC}`"
	echo "	migrate CAF_MANIFEST CAF_CHECKOUT_DIR [-b]"
	echo "	                       Migrates everything specified in a Code Aurora Forum (Qualcomm) CAF_MANIFEST"
	echo "	                       to the Philips Hue github repositories:"
	echo "	                       1. The QSDK is checked out to the CAF_CHECKOUT_DIR using the specified"
	echo "	                          CAF_MANIFEST."
	echo "	                       2. The CAF_MANIFEST is migrated to point to the Philips Hue github"
	echo "	                          repositories."
	echo "	                       3. A pruned version of the CAF_MANIFEST is generated which removes some"
	echo "	                          large unused projects."
	echo "	                       4. If the migrated manifest describes git repos which do not yet exist under"
	echo "	                          the Philips Hue github account, the user is prompted to create these."
	echo "	                       5. For all QSDK repo projects, all new branches and tags are pushed to the"
	echo "	                          Philips Hue github repositories."
	echo "	                       6. The migrated manifests are pushed to the Philips Hue github manifests"
	echo "	                          repository."
	echo "	                       OPTIONS:"
	echo "	                       -b   Push by branch to github: Use a slower, but more robust way to push"
	echo "	                            large repositories."
	echo "All COMMANDS affect the following QSDK repo projects:"
	for p in ${PROJECTS}; do
		echo "	${p}"
	done
}

abortShowHelp() {
	error "$*"
	echo >&2
	showHelp >&2
	exit 1
}

parseMakeVariable() {
	local NAME=$1
	eval "${NAME}=`awk -F '=' '/'${NAME}'[:?]{0,1}=/{print $2}'`"
}

parseQsdkSrc() {
	parseMakeVariable MANIFEST_REPOSITORY <${QSDK_SRC}
	parseMakeVariable MANIFEST_BRANCH <${QSDK_SRC}
	parseMakeVariable MANIFEST_FILE <${QSDK_SRC}
	parseMakeVariable REPO_REPOSITORY <${QSDK_SRC}
	parseMakeVariable REPO_BRANCH <${QSDK_SRC}
}

fetchManifests() {
	local p=${QUALCOMM_DIR}/.repo/manifests
	if ! [ -d ${p}/.git ]; then
		abort "not a git project: ${p}"
	elif ! cd ${p}; then
		abort "cannot cd to: ${p}"
	elif ! git checkout master; then
		abort "cannot checkout master: ${p}"
	elif ! git pull origin; then
		abort "cannot pull from origin: ${p}"
	fi
}

fetch() {
	for p in ${PROJECT_PATHS}; do
		echoYellow "Within $p:"
		if ! [ -d ${p}/.git ]; then
			abort "not a git project: ${p}"
		elif ! cd ${p}; then
			abort "cannot cd to: ${p}"
	elif ! git fetch ${REPO_NAME} --tags $*; then
			abort "cannot fetch: ${p}"
		fi
	done
	echoYellow "Within .repo/manifests:"
	if ! fetchManifests; then
		abort "cannot fetch latest manifests"
	fi
}

push() {
	local BRANCH=$1;shift
	for p in ${PROJECT_PATHS}; do
		echoYellow "Within $p:"
		if ! [ -d ${p}/.git ]; then
			abort "not a git project: ${p}"
		elif ! cd ${p}; then
			abort "cannot cd to: ${p}"
		elif ! git push ${REPO_NAME} ${BRANCH} $*; then
			abort "cannot push: ${p}"
		fi
	done
}

revertQsdk() {
	if ! touch ${QSDK_SRC}; then
		warning "cannot touch ${QSDK_SRC}"
		return 1
	elif ! cd ${OPENWRT_DIR}; then
		warning "cannot cd to ${OPENWRT_DIR}"
		return 1
	elif ! make qsdk.checkout; then
		warning "cannot make qsdk.checkout"
		return 1
	else
		return 0
	fi
}

stash() {
	cd ${QSDK_DIR} || abort "cannot cd to ${QSDK_DIR}"
	abortIfAllProjectsNotOnConsistentBranch
	abortIfUncommittedChanges
	for p in ${PROJECT_PATHS}; do
		echoYellow "Within $p:"
		if ! [ -d ${p}/.git ]; then
			abort "not a git project: ${p}"
		elif ! cd ${p}; then
			abort "cannot cd to: ${p}"
		elif ! git checkout --detach HEAD $*; then
			abort "cannot checkout: ${p}"
		fi
	done
	if ! revertQsdk; then
		abort "cannot revert QSDK repo projects"
	fi
}

checkout() {
	local BRANCH=$1;shift
	for p in ${PROJECT_PATHS}; do
		echoYellow "Within $p:"
		if ! [ -d ${p}/.git ]; then
			abort "not a git project: ${p}"
		elif ! cd ${p}; then
			abort "cannot cd to: ${p}"
		elif ! git checkout ${BRANCH} $*; then
			abort "cannot checkout: ${p}"
		fi
	done
}

status() {
	if ! cd ${QUALCOMM_DIR}; then
		abort "cannot cd to ${QUALCOMM_DIR}"
	elif ! repo status; then
		abort "repo status"
	fi
}

start() {
	local BRANCH=$1
	[ -z "${BRANCH}" ] && abortShowHelp "start: BRANCH not specified"
	if ! cd ${QUALCOMM_DIR}; then
		abort "cannot cd to ${QUALCOMM_DIR}"
	elif ! repo start ${BRANCH} --all; then
		abort "repo start ${BRANCH} ${PROJECTS}"
	else
		echo "All QSDK repo projects branched:"
		showProjectStatus "	"
	fi
}

getBranch() {
	if ! cd ${QSDK_DIR}; then
		abort "cannot cd to ${QSDK_DIR}"
	elif ! repo status; then
		abort "error: 'repo status' failed"
	fi | stripColor | if ! awk '
		BEGIN {
			stderr="/dev/stderr"
		}
		/^project/ {
			project=$2
			refType=$3
			ref=$4
			if(refType != "branch") {
				printf("error: project %s not on a branch: %s\n", project, $0) > stderr
				printf("\tconsider `'${SELF}' start` to fix\n") > stderr
				exit 1
			} else {
				branches[project]=ref
			}
		}
		END {
			p_prev=""
			for(p in branches) {
				if(p_prev == "") {
				} else if(branches[p] != branches[p_prev]) {
					printf("error: project branches inconsistent:\n") > stderr
					printf("\t%s: %s\n", p, branches[p]) > stderr
					printf("\t%s: %s\n", p_prev, branches[p_prev]) > stderr
					printf("\tconsider `'${SELF}' start` to fix\n") > stderr
					exit 1
				}
				p_prev = p
			}
			print branches[p]
		}'; then
		exit 1
	fi
}

showProjectStatus() {
	local PREFIX="$1"
	repo status | stripColor | while read PROJECT; do
		echo "${PREFIX}${PROJECT}"
	done
}

branch() {
	if ! cd ${QSDK_DIR}; then
		abort "cannot cd to ${QSDK_DIR}"
	fi
	local BRANCH=`getBranch 2>/dev/null`
	if [ "$?" -ne "0" ]; then
		error "not all QSDK repo projects are on the same branch:"
		showProjectStatus "	" >&2
		exit 1
	elif [ -z "${BRANCH}" ]; then
		abort "QSDK repo projects are not on any branch"
	else
		local PROJECT
		echo "All QSDK repo projects consistent:"
		showProjectStatus "	"
		echo "Branch is:"
		echo "	${BRANCH}"
	fi
}

abandon() {
	local BRANCH=$1
	[ -z "${BRANCH}" ] && abortShowHelp "abandon: BRANCH not specified"
	if ! cd ${QUALCOMM_DIR}; then
		abort "cannot cd to ${QUALCOMM_DIR}"
	elif ! repo abandon ${BRANCH}; then
		abort "repo abandon ${BRANCH}"
	elif ! revertQsdk; then
		abort "cannot touch ${QSDK_SRC}"
	fi
}

rebase() {
	local MANIFEST=${1%.xml}
	[ -z "${MANIFEST}" ] && abortShowHelp "rebase: MANIFEST not specified"
	if ! cd ${QUALCOMM_DIR}; then
		abort "cannot cd to ${QUALCOMM_DIR}"
	elif ! repo init -u ${MANIFEST_REPOSITORY} -b ${MANIFEST_BRANCH} -m ${MANIFEST}.xml --repo-url=${REPO_REPOSITORY} --repo-branch=${REPO_BRANCH}; then
		abort "cannot init repo to ${MANIFEST}: ${QUALCOMM_DIR}"
	elif ! repo sync; then
		abort "errors syncing repo: ${QUALCOMM_DIR}"
	fi
}

stripColor() {
	sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"
}

abortIfAllProjectsNotOnConsistentBranch() {
	local BRANCH=`getBranch`
	if [ "$?" -ne "0" ]; then
		abort "not all QSDK repo projects are on the same branch"
	elif [ -z "${BRANCH}" ]; then
		abort "QSDK repo projects are not on any branch"
	fi
}

abortIfUncommittedChanges() {
	if ! repo status; then
		abort "error: 'repo status' failed"
	fi | stripColor | if ! awk '
		BEGIN {
			stderr="/dev/stderr"
		}
		/^project/ {
			project=$2
		}
		// {
			if($1 != "project") {
				printf("error: project %s has local changes:\n", project) > stderr
				printf("\tfrom '`pwd`', run `repo status` to to see local changes\n") > stderr
				printf("\tto revert file changes, use `git checkout -- ${filename}`\n") > stderr
				printf("\tto commit file changes, use `git add ${filename}` and `git commit`\n") > stderr
				exit 1
			}
		}'; then
		exit 1
	fi
}

tagAndPushAllQsdkProjects() {
	local MANIFEST=$1
	for p in ${PROJECT_PATHS}; do
		if ! [ -d ${p}/.git ]; then
			abort "not a git project: ${p}"
		elif ! cd ${p}; then
			abort "cannot cd to: ${p}"
		elif ! git tag ${MANIFEST}; then
			abort "cannot tag: ${p}: ${MANIFEST}"
		elif ! git push ${REPO_NAME} refs/tags/${MANIFEST}; then
			abort "cannot push tag: ${p}->${REPO_NAME}: ${MANIFEST}"
		fi
	done
}

createAndPushManifest() {
	local MANIFEST=$1
	local p=${QUALCOMM_DIR}/.repo/manifests
	if ! [ -d ${p}/.git ]; then
		abort "not a git project: ${p}"
	elif ! cd ${p}; then
		abort "cannot cd to: ${p}"
	elif ! git checkout master; then
		abort "cannot checkout master: ${p}"
	elif ! git pull origin; then
		abort "cannot pull from origin: ${p}"
	elif ! repo manifest -r -o ${MANIFEST}.xml; then
		abort "cannot create ${MANIFEST}.xml: ${p}"
	elif ! git add ${MANIFEST}.xml; then
		abort "cannot stage ${MANIFEST}.xml: ${p}"
	elif ! git commit; then
		abort "cannot commit ${MANIFEST}.xml: ${p}"
	elif ! git push origin HEAD; then
		abort "cannot push to origin: ${p}"
	fi
}

updateQsdkSources() {
	local MANIFEST=$1
	if ! sed -i 's#\(MANIFEST_FILE:=\).\+#\1'${MANIFEST}.xml'#g' ${QSDK_SRC}; then
		abort "cannot modify: ${QSDK_SRC}"
	fi
}

continueIfYesAbortIfNo() {
	local MESSAGE="$*"
	local CHOICE
	while read -n 1 -p "${MESSAGE}" CHOICE; do
		echo
		case "${CHOICE}" in
		[nN])
			abort "cannot continue"
			;;
		[yY])
			return 0
			;;
		*)
			error "invalid option: ${CHOICE}"
			;;
		esac
	done
}

abandonBranchIfRequested() {
	local PROMPT="$*"
	if [ -n "${PROMPT}" ]; then
		echo "${PROMPT}"
	fi
	local BRANCH=`getBranch`
	if [ "$?" -ne "0" ]; then
		error "unexpected: not all QSDK repo projects are on the same branch:"
		showProjectStatus "	" >&2
		exit 1
	elif [ -z "${BRANCH}" ]; then
		abort "unexpected: QSDK repo projects are not on any branch"
	else
		continueIfYesAbortIfNo "Abandon branch '${BRANCH}'? (y/n)"
		abandon ${BRANCH} 
	fi
}

commit() {
	local MANIFEST=${1%.xml}
	[ -z "${MANIFEST}" ] && abortShowHelp "commit: MANIFEST not specified"
	cd ${QSDK_DIR} || abort "cannot cd to ${QSDK_DIR}"
	abortIfAllProjectsNotOnConsistentBranch
	abortIfUncommittedChanges
	tagAndPushAllQsdkProjects ${MANIFEST}
	createAndPushManifest ${MANIFEST}
	updateQsdkSources ${MANIFEST}
	abandonBranchIfRequested "All changes committed. It is recommended to abort the current branch. Not doing so" \
							 "will cause unexpected rebases when checking out older versions."
}

ls-commits() {
	local filename
	local p=${QUALCOMM_DIR}/.repo/manifests
	if ! [ -d ${p}/.git ]; then
		abort "not a git project: ${p}"
	elif ! cd ${p}; then
		abort "cannot cd to: ${p}"
	elif ! git checkout -q master; then
		abort "cannot checkout master: ${p}"
	elif ! git pull -q origin; then
		abort "cannot pull from origin: ${p}"
	elif ! git ls-files; then
		abort "cannot pull from origin: ${p}"
	fi | while read filename; do
		echo "$(cd $p && git log -1 --date=iso --format="%ad" -- $filename) $filename"
	done | sort 
}

migrate() {
	local CAF_MANIFEST=$1;shift
	[ -z "${CAF_MANIFEST}" ] && abortShowHelp "migrate: CAF_MANIFEST not specified"
	local CAF_CHECKOUT_DIR=$1;shift
	[ -z "${CAF_CHECKOUT_DIR}" ] && abortShowHelp "migrate: CAF_CHECKOUT_DIR not specified"
	if ! mkdir -p ${CAF_CHECKOUT_DIR}; then
		abort "cannot create directory: ${CAF_CHECKOUT_DIR}"
	elif ! cd ${CAF_CHECKOUT_DIR}; then
		abort "cannot cd to: ${CAF_CHECKOUT_DIR}"
	elif ! ${QSDK_TOOLS_DIR}/migrateManifestAndSources.sh -m ${CAF_MANIFEST} $*; then
		abort "cannot migrate: ${CAF_MANIFEST}"
	fi
}

getRepoProjectPaths() {
	cd ${QSDK_DIR}
	if ! repo info; then
		abort "error: 'repo info' failed"
	fi | stripColor | if ! awk '
		/^Mount path:/ {
			print $3
		}'; then
		exit 1
	fi
}

stripBase() {
	local BASE=$1;shift
	local DIR
	for DIR in $*; do
		echo ${DIR#${BASE}/}/
	done
}		

PROJECT_PATHS="`getRepoProjectPaths`"
PROJECTS="`stripBase ${QUALCOMM_DIR} ${PROJECT_PATHS}`"

COMMAND=$1
if [ -z "${COMMAND}" ]; then
	abortShowHelp "COMMAND not specified"
else
	shift
fi

parseQsdkSrc

case "${COMMAND}" in
help)
	showHelp
	;;
fetch)
	fetch $*
	;;
status)
	status $*
	;;
start)
	start $*
	;;
push)
	push $*
	;;
branch)
	branch $*
	;;
stash)
	stash $*
	;;
checkout)
	checkout $*
	;;
abandon)
	abandon $*
	;;
rebase)
	rebase $*
	;;
commit)
	commit $*
	;;
ls-commits)
	ls-commits $*
	;;
migrate)
	migrate $*
	;;
*)
	abortShowHelp "COMMAND not supported: ${COMMAND}"
	;;
esac

exit 0
