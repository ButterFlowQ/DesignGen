import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  JsonView,
  allExpanded,
  darkStyles,
  // defaultStyles,
} from "react-json-view-lite";

/**
 * A component that fetches and displays:
 * 1. The document (HTML) content.
 * 2. The list of chat messages.
 */
function DocumentView() {
  const { documentId } = useParams();
  const [docData, setDocData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newMessage, setNewMessage] = useState("");
  const [toId, setToId] = useState(""); // State to hold the selected recipient ID

  // Simulated recipient list (replace with actual data fetching if needed)
  const recipients = [
    { id: "1", name: "Functional Requirement" },
    { id: "2", name: "Non functional Requirement" },
    { id: "3", name: "Architecture" },
    { id: "4", name: "Api Contract" },
    { id: "5", name: "Database Schema" },
  ];
  console.log(documentId);

  useEffect(() => {
    async function fetchDoc() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/orchestrator/get_document/${documentId}`,
          { mode: "cors" }
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setDocData(data);
      } catch (error) {
        console.error("Error fetching doc:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchDoc();
  }, [documentId]);

  const sendMessage = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/orchestrator/send_chat_message/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: newMessage,
            from_id: "1",
            to_id: toId,
            document_id: documentId,
            conversation_id: docData.current_conversation_id,
          }),
          mode: "cors",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to send message");
      }
      const result = await response.json();
      setDocData({
        ...docData,
        document: result.document,
        chat_messages: [...docData.chat_messages, ...result.chat_messages],
      });
      setNewMessage(""); // Clear input after sending
      setToId(""); // Optionally reset the recipient selection
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!docData) {
    return <div>Error: No document data found.</div>;
  }

  const { chat_messages, document } = docData;

  return (
    <div style={styles.container}>
      {/* Document panel */}
      <div style={styles.docPanel}>
        {/* If it's HTML, you can render with dangerouslySetInnerHTML */}
        <JsonView
          data={JSON.parse(document)}
          shouldExpandNode={allExpanded}
          style={darkStyles}
        />
        {/* <div dangerouslySetInnerHTML={{ __html: document }} /> */}
      </div>

      {/* Chat panel */}
      <div style={styles.chatPanel}>
        <h2>Chat Messages</h2>
        {chat_messages.map((msg) => (
          <div key={msg.id} style={styles.chatMessage}>
            <p>
              <strong>
                From: {msg.from_id} &rarr; To: {msg.to_id}
              </strong>
            </p>
            <p>{msg.message}</p>
          </div>
        ))}
        <div>
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message here..."
            style={{ width: "50%", marginRight: "10px" }}
          />
          <select
            value={toId}
            onChange={(e) => setToId(e.target.value)}
            style={{ width: "20%", marginRight: "10px" }}
          >
            <option value="">Select Recipient</option>
            {recipients.map((recipient) => (
              <option key={recipient.id} value={recipient.id}>
                {recipient.name}
              </option>
            ))}
          </select>
          <button onClick={sendMessage} style={{ width: "20%" }}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "row",
    width: "100vw",
    height: "100vh",
  },
  docPanel: {
    flex: 2,
    borderRight: "1px solid #ccc",
    padding: "1rem",
    overflowY: "auto",
  },
  chatPanel: {
    flex: 1,
    padding: "1rem",
    overflowY: "auto",
  },
  chatMessage: {
    marginBottom: "1rem",
    padding: "0.5rem",
    borderBottom: "1px solid #eee",
  },
};

export default DocumentView;
