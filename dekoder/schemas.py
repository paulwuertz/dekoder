format_schema = {
     "type" : "object",
     "properties" : {
         "name" : {"type" : "string"},
         "lang" : {"type" : "string"},
         "json" : {
            "type" : "array",
            "items" : {
            "anyOf": [
                    {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                ]
             },
         },
    }
 }