from sqlalchemy.sql import func
from config import app,db

## ALL TYPES OF HARDWARE/PROFILES TO CREATE A ROUTER HERE:

class router_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(45))
    num_slots = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())    
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    routers_of_this_type = db.relationship('routers', back_populates='router_type')             # bidirectionally confirmed

class linecard_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(45))
    description = db.Column(db.String(255))
    num_ports = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())    
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    routers_with_linecard = db.relationship('linecards', back_populates='linecard_type')        # bidirectionally confirmed

class interface_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linecard_id = db.Column(db.Integer, db.ForeignKey('linecard_types.id'))
    description = db.Column(db.String(80))
    speed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    interfaces_with_type = db.relationship('interfaces', back_populates='interface_type')       # bidirectionally confirmed

class int_profile_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    profile_type = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    interfaces_with_profile= db.relationship('interfaces', back_populates='int_profile')        # bidirectionally confirmed

# INDIVUAL ELEMENTS 

class linecards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.Integer,db.ForeignKey('routers.id'))
    linecard_type_id = db.Column(db.Integer, db.ForeignKey('linecard_types.id'))
    router_slot = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())    
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    linecard_type = db.relationship('linecard_types', back_populates='routers_with_linecard')   # bidirectionally confirmed
    installed_in_router = db.relationship('routers', back_populates='linecards_installed')      # bidirectionally confirmed
    interfaces_installed = db.relationship('interfaces', back_populates='installed_in_linecards')# bidirectionally confirmed

class interfaces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linecard_id = db.Column(db.Integer, db.ForeignKey('linecards.id'))
    interface_type_id = db.Column(db.Integer, db.ForeignKey('interface_types.id'))
    int_profile_type_id = db.Column(db.Integer, db.ForeignKey('int_profile_types.id'))
    linecard_port_num = db.Column(db.Integer)
    ip_address_v4 = db.Column(db.String(15))
    ip_snm_v4 = db.Column(db.String(15))
    comment = db.Column(db.String(255))
    installed_in_linecards = db.relationship('linecards', back_populates='interfaces_installed')# bidirectionally confirmed
    int_profile = db.relationship('int_profile_types', back_populates='interfaces_with_profile')# bidirectionally confirmed
    interface_type = db.relationship('interface_types', back_populates='interfaces_with_type')  # bidirectionally confirmed

# ACTUAL ROUTER

class routers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    router_type_id = db.Column(db.Integer, db.ForeignKey('router_types.id'))
    linecards_installed = db.relationship('linecards', back_populates='installed_in_router')    # bidirectionally confirmed    
    router_type = db.relationship('router_types', back_populates='routers_of_this_type')        # bidirectionally confirmed