from marshmallow import Schema, fields


class GptRequestSchema(Schema):
    """Schema for GPTRequest"""
    message = fields.Str()