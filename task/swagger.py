from . import serializers

Task = {
    'tags': ['Task'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Task',
                    'description': 'create task for user',
                    'request_body': serializers.Task.CreateSwagger,
                    'responses': {
                        200: serializers.Task.Create
                    }
                },
            }
        },
        'Update': {
            'methods': {
                'put': {
                    'title': 'Update Task',
                    'description': 'update task',
                    'request_body': serializers.Task.UpdateRequestBody,
                    'responses': {
                        200: serializers.Task.Update
                    }
                },
            }
        },
        'List': {
            'methods': {
                'get': {
                    'title': 'Get Tasks',
                    'description': 'get user tasks',
                    'query_serializer': serializers.Task.ListRequestParameter,
                    'responses': {
                        200: serializers.Task.Get(many=True)
                    },
                },
            }
        },
        'Retrieve': {
            'methods': {
                'get': {
                    'title': 'Get Task Detail',
                    'description': 'get task detail',
                    'responses': {
                        200: serializers.Task.Get
                    },
                },
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete Task',
                    'description': 'delete task',
                    'responses': {
                        200: serializers.Task.Delete
                    },
                }
            }
        }
    }
}

TaskFile = {
    'tags': ['Task'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Task File',
                    'description': 'create file attach',
                    'request_body': serializers.TaskFile.CreateRequestBody,
                    'responses': {
                        200: serializers.TaskFile.Create
                    }
                },
            }
        },
        'Update': {
            'methods': {
                'put': {
                    'title': 'Update Task File',
                    'description': 'update file attach',
                    'request_body': serializers.TaskFile.UpdateRequestBody,
                    'responses': {
                        200: serializers.TaskFile.Update
                    }
                },
            }
        },
        'Retrieve': {
            'methods': {
                'get': {
                    'title': 'Get Task File',
                    'description': 'get file attach',
                    'responses': {
                        200: serializers.TaskFile.Get
                    }
                },
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete Task File',
                    'description': 'delete file attach',
                    'request_body': serializers.TaskFile.DeleteRequestBody,
                    'responses': {
                        200: serializers.TaskFile.Delete
                    }
                },
            }
        }
    },
}

TaskResponse = {
    'tags': ['Task Response'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Task Response',
                    'description': 'create task response',
                    'request_body': serializers.TaskResponse.CreateRequestBody,
                    'responses': {
                        200: serializers.TaskResponse.Create
                    }
                },
            }
        },
        'Update': {
            'methods': {
                'put': {
                    'title': 'Update Task Response',
                    'description': 'update task response',
                    'request_body': serializers.TaskResponse.UpdateRequestBody,
                    'responses': {
                        200: serializers.TaskResponse.Update
                    }
                },
            }
        },
        'Retrieve': {
            'methods': {
                'get': {
                    'title': 'Get Task Response',
                    'description': 'get task response',
                    'responses': {
                        200: serializers.TaskResponse.Get
                    }
                },
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete Task Response',
                    'description': 'delete task response',
                    'request_body': serializers.TaskResponse.DeleteRequestBody,
                    'responses': {
                        200: serializers.TaskResponse.Delete
                    }
                },
            }
        }
    },
}

TaskResponseFile = {
    'tags': ['Task Response'],
    'views': {
        'Create': {
            'methods': {
                'post': {
                    'title': 'Create Task Response File',
                    'description': 'create a file for task response',
                    'request_body': serializers.TaskResponseFile.CreateRequestBody,
                    'responses': {
                        200: serializers.TaskResponseFile.Create
                    }
                }
            }
        },
        'Update': {
            'methods': {
                'put': {
                    'title': 'Update Task Response File',
                    'description': 'update task response file',
                    'request_body': serializers.TaskResponseFile.UpdateRequestBody,
                    'responses': {
                        200: serializers.TaskResponseFile.Update
                    }
                }
            }
        },
        'Retrieve': {
            'methods': {
                'get': {
                    'title': 'Get Task Response File',
                    'description': 'get task response file',
                    'responses': {
                        200: serializers.TaskResponseFile.Get
                    }
                }
            }
        },
        'Delete': {
            'methods': {
                'delete': {
                    'title': 'Delete Task Response File',
                    'description': 'delete task response file',
                    'responses': {
                        200: serializers.TaskResponseFile.Delete
                    }
                }
            }
        }
    }
}
