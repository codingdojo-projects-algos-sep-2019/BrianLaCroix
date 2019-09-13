from config import app
from controller_functions import *


# HOME PAGE - INDEX
app.add_url_rule("/", view_func=index)

# HOME PAGE - ROUTER SEARCH
app.add_url_rule("/routers/search", view_func=router_search, methods=["POST"])

# ROUTER TYPES
app.add_url_rule("/router_types/index", view_func=router_types_index, methods=["POST"])
app.add_url_rule("/router_type/add", view_func=router_type_add, methods=["POST"])
app.add_url_rule("/router_type/delete/<int:router_type_id>", view_func=router_type_delete, methods=["POST"])

# LINECARD TYPES
app.add_url_rule("/linecard_types/index", view_func=linecard_types_index, methods=["POST"])
app.add_url_rule("/linecard_type/add", view_func=linecard_type_add, methods=["POST"])
app.add_url_rule("/linecard_type/delete/<int:linecard_type_id>", view_func=linecard_type_delete, methods=["POST"])

# INTERFACE TYPES
app.add_url_rule("/interface_types/index", view_func=interface_types_index, methods=["POST"])
app.add_url_rule("/interface_type/add", view_func=interface_type_add, methods=["POST"])
app.add_url_rule("/interface_type/delete/<int:interface_type_id>", view_func=interface_type_delete, methods=["POST"])

# INT_PROFILE TYPES
app.add_url_rule("/int_profile_types/index", view_func=int_profile_types_index, methods=["POST"])
app.add_url_rule("/int_profile_type/add", view_func=int_profile_types_add, methods=["POST"])
app.add_url_rule("/int_profile_type/delete/<int:int_profile_type_id>", view_func=int_profile_types_delete, methods=["POST"])

# ROUTERS 
app.add_url_rule("/router/index", view_func=router_index, methods=["POST"])
app.add_url_rule("/router/add", view_func=router_add, methods=["POST"])
app.add_url_rule("/router/delete/<int:router_id>", view_func=router_delete, methods=["POST"])
app.add_url_rule("/router/edit/<int:router_id>", view_func=router_edit, methods=["POST"])
app.add_url_rule("/router/update/<int:router_id>",view_func=router_update, methods=["POST"])

