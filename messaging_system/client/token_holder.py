# Module global holder of token; note that this module's members
# cannot be imported using 'from token_holder import token' since that
# just creates a local context of the variable; to get the value by reference
# just import token_holder and use the token_holder.token reference each time
token = None