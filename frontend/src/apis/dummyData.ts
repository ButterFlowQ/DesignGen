// Dummy data for development and error cases
export const dummyData = {
  chat_messages: [
    {
      id: 250,
      message: "Generate code for the same",
      from_id: null,
      to_id: "7",
      is_user_message: true,
      creation_time: "2025-02-02T11:15:45.500Z"
    },
    {
      id: 251,
      message: "Code is generated successfully!",
      from_id: "7",
      to_id: null,
      is_user_message: false,
      creation_time: "2025-02-02T11:15:55.582Z"
    }
  ],
  conversation_id: 68,
  document: JSON.stringify({
    "functional requirements": [
      "User registration and authentication",
      "Document creation and management",
      "Real-time collaboration features",
      "Version control for documents",
      "Search functionality"
    ],
    "non functional requirements": [
      "High availability (99.9% uptime)",
      "Response time under 200ms",
      "Scalable architecture",
      "Data encryption at rest and in transit"
    ]
  })
};