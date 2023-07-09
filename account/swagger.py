from drf_yasg import openapi
from . import serializers

User = {
    'tags': ['Account'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create user',
                    'description': 'create new account | register ',
                    'request_body': serializers.User.CreateRequestBody,
                    'responses': {
                        200: serializers.User.Create,
                    },
                }
            }
        },
        'Login': {
            'methods': {
                'post': {
                    'title': 'Login',
                    'description': 'login and get basic profile',
                    'request_body': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'username': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='your email'
                            ),
                            'password': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='your password'
                            )
                        },
                        required=[
                            'username',
                            'password'
                        ]
                    ),
                    'responses': {
                        200: serializers.User.GetBasic,
                    },
                },
            }
        },
        'UpdateLogin': {
            'methods': {
                'put': {
                    'title': 'Update login - Access Token ',
                    'description': 'get access token by refresh token - keep login',
                    'request_body': serializers.Token.GetRefresh,
                    'responses': {
                        200: serializers.Token.GetAccess,
                    },
                },
            }
        },
        'UpdateUser': {
            'methods': {
                'put': {
                    'title': 'Update user',
                    'description': 'Update user information',
                    'request_body': serializers.User.UpdateRequestBody,
                    'responses': {
                        200: serializers.User.Update,
                    },
                },
            }
        },
        'ResetPassword': {
            'methods': {
                'post': {
                    'title': 'Reset Password',
                    'description': 'Reset password account',
                    'request_body': serializers.User.ResetPasswordRequestBody,
                    'responses': {
                        200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING)
                        })
                    },
                },
            }
        },
        'ResetPasswordCode': {
            'methods': {
                'post': {
                    'title': 'Reset Password Code',
                    'description': 'To reset your password, you need to send the code you received from the email to this endpoint',
                    'request_body': serializers.User.ResetPasswordCodeRequestBody,
                    'responses': {
                        200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING)
                        })
                    },
                },
            }
        },
        'GroupList': {
            'methods': {
                'get': {
                    'title': 'Group List',
                    'description': 'get user groups',
                    'responses': {
                        200: serializers.User.GroupList
                    },
                },
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete User',
                    'description': 'Delete user account',
                    'request_body': serializers.User.DeleteRequestBody,
                    'responses': {
                        200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING, default='Bye Friend...')
                        })
                    },
                },
            }
        }
    }
}

Group = {
    'tags': ['Group'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Group',
                    'description': 'create groups to perform tasks',
                    'request_body': serializers.Group.CreateRequestBody,
                    'responses': {
                        200: serializers.Group.Create
                    },
                },
            }
        },
        'Retrieve': {
            'methods': {
                'get': {
                    'title': 'Retrieve Group',
                    'description': 'get group to perform tasks',
                    'responses': {
                        200: serializers.Group.Get
                    },
                }
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete Group',
                    'description': 'delete group',
                    'responses': {
                        200: serializers.Group.Delete,
                    },
                },
            }
        }
    }
}

GroupUser = {
    'tags': ['Group User'],
    'views': {
        'RequestAddUser': {
            'methods': {
                'post': {
                    'title': 'Request Add User to Group',
                    'description': 'add user(member) to group',
                    'request_body': serializers.GroupUser.AddUserRequestBody,
                    'responses': {
                        200: serializers.GroupUser.AddUser,
                    },
                },
            }
        },
        'AcceptRequestJoin': {
            'methods': {
                'get': {
                    'title': 'Accept Request Join To Group',
                    'description': 'accept request join to group',
                    'responses': {
                        200: serializers.GroupUser.AcceptRequestJoin
                    },
                },
            }
        },
        'List':{
            'methods':{
                'get':{
                    'title': 'Group members',
                    'description': 'get users(memberships) from group',
                    'responses': {
                        200: serializers.GroupUser.List,
                    },
                }
            }
        },
        'Kick': {
            'methods': {
                'delete': {
                    'title': 'Kick User Group',
                    'description': 'kick user(membership) from group',
                    'responses': {
                        200: serializers.GroupUser.Kick,
                    },
                },
            }
        }
    }
}

GroupAdmin = {
    'tags': ['Group Admin'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Admin',
                    'description': 'create an admin for group',
                    'request_body': serializers.GroupAdmin.CreateRequestBody,
                    'responses': {
                        200: serializers.GroupAdmin.Create
                    },
                },
            }
        },
        'List': {
            'methods': {
                'get': {
                    'title': 'Get Admins Group',
                    'description': 'get admins group',
                    'responses': {
                        200: serializers.GroupAdmin.Get(many=True),
                    },
                },
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Kick Admin',
                    'description': 'kick admin group',
                    'responses': {
                        200: serializers.GroupAdmin.Kick
                    },
                },
            }
        }
    }
}
