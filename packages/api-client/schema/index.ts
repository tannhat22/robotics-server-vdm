export default {
  openapi: "3.1.0",
  info: { title: "RMF API Server", version: "0.1.0" },
  paths: {
    "/socket.io": {
      get: {
        summary: "Socket.io endpoint",
        description:
          '# NOTE: This endpoint is here for documentation purposes only, this is _not_ a REST endpoint.\n\n## About\nThis exposes a minimal pubsub system built on top of socket.io.\nIt works similar to a normal socket.io endpoint, except that are 2 special\nrooms which control subscriptions.\n\n## Rooms\n### subscribe\nClients must send a message to this room to start receiving messages on other rooms.\nThe message must be of the form:\n\n```\n{\n    "room": "<room_name>"\n}\n```\n\n### unsubscribe\nClients can send a message to this room to stop receiving messages on other rooms.\nThe message must be of the form:\n\n```\n{\n    "room": "<room_name>"\n}\n```',
        operationId: "_lambda__socket_io_get",
        responses: {
          "200": {
            description: "Successful Response",
            content: { "application/json": { schema: {} } },
          },
        },
      },
    },
    "/robots": {
      get: {
        tags: ["Robots"],
        summary: "Get Robots",
        operationId: "get_robots_robots_get",
        responses: {
          "200": {
            description: "Successful Response",
            content: {
              "application/json": {
                schema: {
                  items: { $ref: "#/components/schemas/Robot" },
                  type: "array",
                  title: "Response Get Robots Robots Get",
                },
              },
            },
          },
        },
      },
      post: {
        tags: ["Robots"],
        summary: "Create Robot",
        operationId: "create_robot_robots_post",
        requestBody: {
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/Robot" },
            },
          },
          required: true,
        },
        responses: {
          "201": {
            description: "Successful Response",
            content: { "application/json": { schema: {} } },
          },
          "422": {
            description: "Validation Error",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/HTTPValidationError" },
              },
            },
          },
        },
      },
    },
    "/robots/{id}": {
      get: {
        tags: ["Robots"],
        summary: "Get Robot",
        operationId: "get_robot_robots__id__get",
        parameters: [
          {
            name: "id",
            in: "path",
            required: true,
            schema: { type: "integer", title: "Id" },
          },
        ],
        responses: {
          "200": {
            description: "Successful Response",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/Robot" },
              },
            },
          },
          "422": {
            description: "Validation Error",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/HTTPValidationError" },
              },
            },
          },
        },
      },
      put: {
        tags: ["Robots"],
        summary: "Update Robot",
        operationId: "update_robot_robots__id__put",
        parameters: [
          {
            name: "id",
            in: "path",
            required: true,
            schema: { type: "integer", title: "Id" },
          },
        ],
        requestBody: {
          required: true,
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/Robot" },
            },
          },
        },
        responses: {
          "202": {
            description: "Successful Response",
            content: { "application/json": { schema: {} } },
          },
          "422": {
            description: "Validation Error",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/HTTPValidationError" },
              },
            },
          },
        },
      },
      delete: {
        tags: ["Robots"],
        summary: "Destroy",
        operationId: "destroy_robots__id__delete",
        parameters: [
          {
            name: "id",
            in: "path",
            required: true,
            schema: { type: "integer", title: "Id" },
          },
        ],
        responses: {
          "204": { description: "Successful Response" },
          "422": {
            description: "Validation Error",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/HTTPValidationError" },
              },
            },
          },
        },
      },
    },
  },
  components: {
    schemas: {
      HTTPValidationError: {
        properties: {
          detail: {
            items: { $ref: "#/components/schemas/ValidationError" },
            type: "array",
            title: "Detail",
          },
        },
        type: "object",
        title: "HTTPValidationError",
      },
      Robot: {
        properties: {
          serial_no: {
            type: "string",
            title: "Serial No",
            description: "The serial number is preset at the factory",
          },
          name: { type: "string", title: "Name" },
          ip_address: { type: "string", title: "Ip Address" },
        },
        type: "object",
        required: ["serial_no", "name", "ip_address"],
        title: "Robot",
      },
      ValidationError: {
        properties: {
          loc: {
            items: { anyOf: [{ type: "string" }, { type: "integer" }] },
            type: "array",
            title: "Location",
          },
          msg: { type: "string", title: "Message" },
          type: { type: "string", title: "Error Type" },
        },
        type: "object",
        required: ["loc", "msg", "type"],
        title: "ValidationError",
      },
    },
  },
};
