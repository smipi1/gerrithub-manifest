from json import JSONEncoder
from package import Package
from license import License

class PackageAndLicenseEncoder (JSONEncoder):
  def default (self, obj):
    if isinstance (obj, Package):
      return { 'package'     : obj.name 
             , 'version'     : obj.version
             , 'website'     : obj.website
             , 'licenseFile' : obj.licenses[0].filePath(obj, "")
             }
    elif isinstance (obj, License):
      return ""
    return json.JSONEncoder.default(self, obj)


