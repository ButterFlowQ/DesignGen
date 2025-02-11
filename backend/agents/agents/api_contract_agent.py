from typing import List

from agents.types import AgentType, LLMResponse
from orchestratorV2.models import ChatMessage
from .agent_interface import AgentInterface
from orchestratorV2.models import VersionedDocument


class APIContractAgent(AgentInterface):
    """
    An agent responsible for defining API contracts and interactions in a system design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the APIContractAgent with a system message and response format.
        """
        system_message = """
            You are an API Contracts and Interaction Agent in a system design pipeline. Your role is to:
                1. Define and specify API contracts between system components.
                2. Design interaction protocols for internal and external communications.
                3. Ensure APIs adhere to industry standards and best practices.
                4. Identify and resolve potential integration issues.
                5. Maintain documentation for all API endpoints and interaction flows.
                6. Return the API contracts in Swagger API JSON format.

            Ask as many clarifying questions as needed to understand:
                - The required API endpoints and their purposes.
                - The request/response formats and data structures.
                - The authentication and authorization requirements.
                - The error handling and status codes.
                - The API versioning and backward compatibility needs.

            You will receive a user message and the current state of the complete design document in the following JSON format:

            {
              "document": {
                "functional requirements": [...],
                "non functional requirements": [...],
                "architecture": {...},
                "api contracts": {
                    "swagger": "2.0",
                    "info": {
                        "title": "",
                        "version": ""
                    },
                    "paths": {
                        "<path>": {
                            "get": {
                                "summary": "",
                                "parameters": [
                                    {
                                        "name": "",
                                        "in": "",
                                        "required": true,
                                        "type": "",
                                        "description": ""
                                    }
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful response",
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": { "type": "string" },
                                                "email": { "type": "string" }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "database schema": [...]
              },
              "user message": "User's input or request regarding API contracts"
            }

            For each interaction, you must provide a response in the following JSON format:

            {
                "updated api contracts": {
                    "swagger": "2.0",
                    "info": {
                        "title": "",
                        "version": ""
                    },
                    "paths": {
                        "<path>": {
                            "get": {
                                "summary": "",
                                "parameters": [
                                    {
                                        ...
                                    }
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful response",
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": { "type": "string" },
                                                "email": { "type": "string" }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "communication": "Explanation of changes or reasoning"
            }

            Example:
            {
              "updated api contracts": {
                    "swagger": "2.0",
                    "info": {
                        "title": "Example API",
                        "version": "1.0"
                    },
                    "paths": {
                        "/users/{userId}": {
                            "get": {
                                "summary": "Get user by ID",
                                "parameters": [
                                    {
                                        "name": "userId",
                                        "in": "path",
                                        "required": true,
                                        "type": "integer",
                                        "description": "ID of the user to fetch"
                                    },
                                    ... other parameters
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful response",
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "name": { "type": "string" },
                                                "email": { "type": "string" },
                                            }
                                        }
                                    },
                                    ... other responses
                                }
                            },
                            ... other methods
                        },
                        ... other paths
                    }
                },
                "communication": "Added POST /users endpoint to support user registration"
            }

            Don't update other parts of the document, only the API contracts.

            If the user message does not require any changes to the API contracts,
            return the same API contracts as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        response_format = {
            "updated_doc_element": "updated api contracts",
            "response_message": "communication",
        }
        super().__init__(AgentType.API_CONTRACT, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the chat history and generates a response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated API contracts, communication, and workflow status.
        """
        llm_messages = self.generate_llm_history(chat_history, AgentType.API_CONTRACT)
        # api_contract = VersionedDocument.objects.get(pk=85).document_elements[
        #     "api contracts"
        # ]
        llm_response = self.llm.get_response(llm_messages, self.response_format)
        api_contracts = {
            "swagger": "2.0",
            "info": {
                "title": "E-Commerce Platform API",
                "version": "1.0.0",
                "description": "API documentation for the E-Commerce Platform, facilitating interactions between customers and shopkeepers.",
            },
            "host": "{api.example.com}",
            "basePath": "/v1",
            "schemes": ["https"],
            "paths": {
                "/auth/register": {
                    "post": {
                        "summary": "Register a new user",
                        "description": "Registers a new user (customer or shopkeeper) with necessary details including role.",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "in": "body",
                                "name": "body",
                                "description": "User registration details",
                                "required": True,
                                "schema": {"$ref": "#/definitions/RegisterRequest"},
                            }
                        ],
                        "responses": {
                            "201": {
                                "description": "User registered successfully",
                                "schema": {"$ref": "#/definitions/User"},
                            },
                            "400": {"description": "Invalid input"},
                        },
                    }
                },
                "/auth/login": {
                    "post": {
                        "summary": "User login",
                        "description": "Authenticates a user and returns a JWT token for authorized access.",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "in": "body",
                                "name": "body",
                                "description": "User login credentials",
                                "required": True,
                                "schema": {"$ref": "#/definitions/LoginRequest"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Login successful",
                                "schema": {"$ref": "#/definitions/AuthResponse"},
                            },
                            "401": {"description": "Authentication failed"},
                        },
                    }
                },
                "/auth/logout": {
                    "post": {
                        "summary": "User logout",
                        "description": "Logs out the authenticated user and invalidates the JWT token.",
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "in": "header",
                                "name": "Authorization",
                                "type": "string",
                                "required": True,
                                "description": "JWT token",
                            }
                        ],
                        "responses": {
                            "200": {"description": "Logout successful"},
                            "401": {"description": "Unauthorized"},
                        },
                    }
                },
                "/shopkeepers": {
                    "get": {
                        "summary": "List all shopkeepers",
                        "description": "Retrieves a list of all shopkeepers available on the platform.",
                        "produces": ["application/json"],
                        "responses": {
                            "200": {
                                "description": "A list of shopkeepers",
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/definitions/User"},
                                },
                            }
                        },
                    }
                },
                "/shopkeepers/{shopkeeperId}/inventory": {
                    "get": {
                        "summary": "Get shopkeeper's inventory",
                        "description": "Retrieves the inventory items for a specific shopkeeper.",
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "shopkeeperId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the shopkeeper",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Inventory items",
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/definitions/InventoryItem"},
                                },
                            },
                            "404": {"description": "Shopkeeper not found"},
                        },
                    },
                    "post": {
                        "summary": "Add inventory item",
                        "description": "Adds a new item to the specified shopkeeper's inventory. (Shopkeeper only)",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "shopkeeperId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the shopkeeper",
                            },
                            {
                                "in": "body",
                                "name": "body",
                                "description": "Inventory item details",
                                "required": True,
                                "schema": {"$ref": "#/definitions/AddItemRequest"},
                            },
                        ],
                        "responses": {
                            "201": {
                                "description": "Item added successfully",
                                "schema": {"$ref": "#/definitions/InventoryItem"},
                            },
                            "400": {"description": "Invalid input"},
                            "403": {"description": "Forbidden"},
                        },
                    },
                },
                "/shopkeepers/{shopkeeperId}/inventory/{itemId}": {
                    "put": {
                        "summary": "Update inventory item",
                        "description": "Updates details of a specific inventory item for the shopkeeper. (Shopkeeper only)",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "shopkeeperId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the shopkeeper",
                            },
                            {
                                "name": "itemId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the inventory item",
                            },
                            {
                                "in": "body",
                                "name": "body",
                                "description": "Updated inventory item details",
                                "required": True,
                                "schema": {"$ref": "#/definitions/UpdateItemRequest"},
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Item updated successfully",
                                "schema": {"$ref": "#/definitions/InventoryItem"},
                            },
                            "400": {"description": "Invalid input"},
                            "403": {"description": "Forbidden"},
                            "404": {"description": "Item not found"},
                        },
                    },
                    "delete": {
                        "summary": "Delete inventory item",
                        "description": "Removes an item from the shopkeeper's inventory. (Shopkeeper only)",
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "shopkeeperId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the shopkeeper",
                            },
                            {
                                "name": "itemId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the inventory item",
                            },
                        ],
                        "responses": {
                            "204": {"description": "Item deleted successfully"},
                            "403": {"description": "Forbidden"},
                            "404": {"description": "Item not found"},
                        },
                    },
                },
                "/orders": {
                    "post": {
                        "summary": "Place a new order",
                        "description": "Places a new order by a customer for multiple items from a specific shopkeeper.",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "in": "body",
                                "name": "body",
                                "description": "Order details",
                                "required": True,
                                "schema": {"$ref": "#/definitions/PlaceOrderRequest"},
                            }
                        ],
                        "responses": {
                            "201": {
                                "description": "Order placed successfully",
                                "schema": {"$ref": "#/definitions/Order"},
                            },
                            "400": {"description": "Invalid input"},
                            "404": {"description": "Shopkeeper or items not found"},
                        },
                    },
                    "get": {
                        "summary": "List orders",
                        "description": "Retrieves a list of orders for the authenticated user, filtered by role (customer or shopkeeper).",
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "in": "header",
                                "name": "Authorization",
                                "type": "string",
                                "required": True,
                                "description": "JWT token",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "A list of orders",
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/definitions/Order"},
                                },
                            },
                            "401": {"description": "Unauthorized"},
                        },
                    },
                },
                "/orders/{orderId}": {
                    "get": {
                        "summary": "Get order details",
                        "description": "Retrieves detailed information for a specific order, including items, prices, and timestamps.",
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "orderId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the order",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Order details",
                                "schema": {"$ref": "#/definitions/Order"},
                            },
                            "404": {"description": "Order not found"},
                        },
                    }
                },
                "/orders/{orderId}/status": {
                    "put": {
                        "summary": "Update order status",
                        "description": "Updates the status of a specific order (e.g., created, processing, cancelled, fulfilled). (Shopkeeper only)",
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "orderId",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "format": "uuid",
                                "description": "ID of the order",
                            },
                            {
                                "in": "body",
                                "name": "body",
                                "description": "Status update details",
                                "required": True,
                                "schema": {"$ref": "#/definitions/UpdateStatusRequest"},
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Order status updated successfully",
                                "schema": {"$ref": "#/definitions/Order"},
                            },
                            "400": {"description": "Invalid status value"},
                            "403": {"description": "Forbidden"},
                            "404": {"description": "Order not found"},
                        },
                    }
                },
            },
            "definitions": {
                "RegisterRequest": {
                    "type": "object",
                    "required": ["username", "email", "password", "role"],
                    "properties": {
                        "username": {"type": "string", "example": "akash123"},
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "akash.singh@gmail.com.com",
                        },
                        "password": {
                            "type": "string",
                            "format": "password",
                            "example": "SecurePass123",
                        },
                        "role": {
                            "type": "string",
                            "enum": ["customer", "shopkeeper"],
                            "example": "customer",
                        },
                    },
                },
                "LoginRequest": {
                    "type": "object",
                    "required": ["email", "password"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "john@example.com",
                        },
                        "password": {
                            "type": "string",
                            "format": "password",
                            "example": "SecurePass123",
                        },
                    },
                },
                "AuthResponse": {
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string",
                            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                        }
                    },
                },
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "123e4567-e89b-12d3-a456-426614174000",
                        },
                        "username": {"type": "string", "example": "john_doe"},
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "john@example.com",
                        },
                        "role": {
                            "type": "string",
                            "enum": ["customer", "shopkeeper"],
                            "example": "customer",
                        },
                        "createdAt": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2023-10-05T14:48:00.000Z",
                        },
                    },
                },
                "InventoryItem": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "223e4567-e89b-12d3-a456-426614174001",
                        },
                        "shopkeeperId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "123e4567-e89b-12d3-a456-426614174000",
                        },
                        "name": {"type": "string", "example": "Wireless Mouse"},
                        "price": {
                            "type": "number",
                            "format": "float",
                            "example": 29.99,
                        },
                        "imageUrl": {
                            "type": "string",
                            "format": "url",
                            "example": "https://example.com/images/mouse.jpg",
                        },
                        "createdAt": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2023-10-05T14:50:00.000Z",
                        },
                    },
                },
                "AddItemRequest": {
                    "type": "object",
                    "required": ["name", "price", "image_url"],
                    "properties": {
                        "name": {"type": "string", "example": "Wireless Keyboard"},
                        "price": {
                            "type": "number",
                            "format": "float",
                            "example": 49.99,
                        },
                        "image_url": {
                            "type": "string",
                            "format": "url",
                            "example": "https://example.com/images/keyboard.jpg",
                        },
                    },
                },
                "UpdateItemRequest": {
                    "type": "object",
                    "required": ["name", "price", "image_url"],
                    "properties": {
                        "name": {"type": "string", "example": "Bluetooth Keyboard"},
                        "price": {
                            "type": "number",
                            "format": "float",
                            "example": 59.99,
                        },
                        "image_url": {
                            "type": "string",
                            "format": "url",
                            "example": "https://example.com/images/bluetooth_keyboard.jpg",
                        },
                    },
                },
                "PlaceOrderRequest": {
                    "type": "object",
                    "required": ["shopkeeperId", "items"],
                    "properties": {
                        "shopkeeperId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "123e4567-e89b-12d3-a456-426614174000",
                        },
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/OrderItemRequest"},
                        },
                    },
                },
                "OrderItemRequest": {
                    "type": "object",
                    "required": ["itemId", "quantity"],
                    "properties": {
                        "itemId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "223e4567-e89b-12d3-a456-426614174001",
                        },
                        "quantity": {"type": "integer", "example": 2},
                    },
                },
                "Order": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "323e4567-e89b-12d3-a456-426614174002",
                        },
                        "customerId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "123e4567-e89b-12d3-a456-426614174000",
                        },
                        "shopkeeperId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "423e4567-e89b-12d3-a456-426614174003",
                        },
                        "status": {
                            "type": "string",
                            "enum": ["created", "processing", "cancelled", "fulfilled"],
                            "example": "created",
                        },
                        "createdAt": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2023-10-05T15:00:00.000Z",
                        },
                        "updatedAt": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2023-10-05T15:00:00.000Z",
                        },
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/OrderItem"},
                        },
                    },
                },
                "OrderItem": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                            "example": "523e4567-e89b-12d3-a456-426614174004",
                        },
                        "orderId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "323e4567-e89b-12d3-a456-426614174002",
                        },
                        "inventoryItemId": {
                            "type": "string",
                            "format": "uuid",
                            "example": "223e4567-e89b-12d3-a456-426614174001",
                        },
                        "quantity": {"type": "integer", "example": 2},
                        "priceAtOrder": {
                            "type": "number",
                            "format": "float",
                            "example": 29.99,
                        },
                        "createdAt": {
                            "type": "string",
                            "format": "date-time",
                            "example": "2023-10-05T15:00:00.000Z",
                        },
                    },
                },
                "UpdateStatusRequest": {
                    "type": "object",
                    "required": ["status"],
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["created", "processing", "cancelled", "fulfilled"],
                            "example": "processing",
                        }
                    },
                },
            },
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Enter your bearer token in the format **Bearer <token>**",
                }
            },
            "security": [{"Bearer": []}],
        }

        llm_response["updated_doc_element"] = api_contracts
        # llm_response["updated_doc_element"] = api_contract
        return llm_response
