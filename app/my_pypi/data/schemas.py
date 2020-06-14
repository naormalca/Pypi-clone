from marshmallow import Schema, fields

#TODO: releases
class PackageSchema(Schema):
    id = fields.Str(dump_only=True)
    created_date = fields.DateTime(dump_only=True)
    last_updated =  fields.DateTime(dump_only=True)
    summary = fields.Str()
    description = fields.Str()
    home_page = fields.Str()
    docs_url = fields.Str()
    package_url = fields.Str()
    author_name = fields.Str()
    author_email = fields.Str()
    license = fields.Str()

class ReleaseSchema(Schema):
    id = fields.Int(dump_only=True)
    version = fields.Method('format_version', dump_only=True)
    created_date = fields.DateTime(dump_only=True)
    package = fields.Nested(PackageSchema, only=('id', 'summary'))

    def format_version(self, release):
        return '{}.{}.{}'.format(release.major_ver, release.minor_ver, release.build_ver)
