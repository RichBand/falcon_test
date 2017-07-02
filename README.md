dev_server.py
    -create the server and set the ports
    -instantiate and set Application() as the application to be called on the refined route/port

<package_name>/
    __init__.py
        -empty

    server.py {Application}
        -inherit from falcon.API
        -define and instantiate the middleware components (DatabaseComponent & ContentComponent)
        -instantiate falcon.API
        -define the routes and the resources to be called in the REST schema of: Collection, Item

    components/
        __init__.py
            - import the Components, define the access to them trough __slots__

        content.py {ContentComponent}
            -define the content_type for the process_response e.g. 'application/json'

        database.py {DatabaseComponent}
            -define the database package to be used e.g. sqlite or SQLAlchemy
            -define the connection necessary to implement CRUD operations
            -open the DB connection on every process_request
            -close the DB connection on every process_response

    models/
        __init__.py
            -empty

        <model_name>.py

            <model_name>Model e.g. {RoutesModel}
                -inherit from declarative_base [sqlalchemy.ext.declarative]
                -define the sqlalchemy ORM interface

            <schema_name>Schema e.g. {RoutesSchema}
                -inherit from Schema [marshmallow.Schema]
                -provide methods to serialize and deserialize, validate, and so on, for the objects <model_name>Model

    resources/
        -implement the REST API philosophy
        __init__.py
            - import the version(s), define the access trough __slots__

        <version>/ e.g. v1
            __init__.py
                -import the resource(s), define the access trough __slots__

            <resource>/ e.g. routes/
                -__init__.py
                    - import the Collection and Item, define the access trough __slots__

                -<resource>.py e.g. route.py
                    -import the model and schema (from <~/package_name>/models/<model_name>.py)
                    -define and implement HTTP methods for each resource e.g. [on_get, on_post, on_put, on_delete]
