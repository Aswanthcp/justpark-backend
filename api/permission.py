from rest_framework.permissions import BasePermission



class IsUserRole(BasePermission):
    def  has_permission(self, request, view):
        request_role_map = {
            'list':['admin','customer','staff','support'],
            'create': ['admin',],
            'retrieve':['admin','staff','support'],
            'update':['admin'],
            'partial_update':[ 'admin' ],
            'destroy': [ 'admin']
        }
        required_roles = request_role_map.get(view.action,[])
        return (request.MyUser.role in required_roles)