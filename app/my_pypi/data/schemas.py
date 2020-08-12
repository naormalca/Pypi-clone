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

class PackageDetailsSchema(Schema):
    package = fields.Nested(PackageSchema)
    latest_release = fields.Nested(ReleaseSchema, exclude=("package",))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    email = fields.String()
    hashed_password = fields.String()
    created_date = fields.DateTime(dump_only=True)
    profile_image_url = fields.String()
    last_login = fields.DateTime(dump_only=True)