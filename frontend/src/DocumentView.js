import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  JsonView,
  allExpanded,
  darkStyles,
  // defaultStyles,
} from "react-json-view-lite";
import "react-chat-elements/dist/main.css";
import { MessageBox } from "react-chat-elements";
import logo from "./logo.png"; // Make sure the path is correct
import Markdown from "react-markdown";

/**
 * A component that fetches and displays:
 * 1. The document (HTML) content.
 * 2. The list of chat messages.
 */
function DocumentView() {
  const { documentId } = useParams();
  const [docData, setDocData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [messageSending, setMessageSending] = useState(false);
  const [newMessage, setNewMessage] = useState("");
  const [toId, setToId] = useState(""); // State to hold the selected recipient ID
  const [history, setHistory] = useState([]);
  const [redoStack, setRedoStack] = useState([]);

  // Simulated recipient list (replace with actual data fetching if needed)
  const recipients = [
    { id: "1", name: "Functional Requirement" },
    { id: "2", name: "Non functional Requirement" },
    { id: "3", name: "Architecture" },
    { id: "4", name: "Api Contract" },
    { id: "5", name: "Database Schema" },
    { id: "6", name: "Java LLD" },
    { id: "7", name: "Java Code" },
    { id: "8", name: "React LLD" },
    { id: "9", name: "React Code" },
  ];
  // console.log(documentId);

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
    setMessageSending(true);
    try {
      console.log(docData);
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
            conversation_id: docData.conversation_id,
          }),
          mode: "cors",
        }
      );
      setMessageSending(false);
      if (!response.ok) {
        throw new Error("Failed to send message");
      }
      const result = await response.json();
      setHistory([...history, docData]); // Save current state to history
      setDocData({
        ...docData,
        document: result.document,
        html_document: result.html_document,
        conversation_id: result.conversation_id,
        chat_messages: [...docData.chat_messages, ...result.chat_messages],
      });
      setNewMessage(""); // Clear input after sending
      setToId(""); // Optionally reset the recipient selection
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const resetConversation = () => {
    setHistory([...history, docData]); // Save current state to history
    setDocData({
      document: docData.document,
      html_document: docData.html_document,
      chat_messages: [],
    });
  };

  const undo = () => {
    if (history.length > 0) {
      const previousState = history.pop();
      setRedoStack([...redoStack, docData]); // Save current state to redo stack
      setDocData(previousState);
      setHistory(history);
    }
  };

  const redo = () => {
    if (redoStack.length > 0) {
      const nextState = redoStack.pop();
      setHistory([...history, docData]); // Save current state to history
      setDocData(nextState);
      setRedoStack(redoStack);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

  if (!docData) {
    return <div style={styles.error}>Error: No document data found.</div>;
  }

  const { chat_messages, document } = docData;

  return (
    <div style={styles.pageContainer}>
      {/* Navbar */}
      <nav style={styles.navbar}>
        <img src={logo} alt="Logo" style={styles.logo} />
        <div style={styles.navButtonsContainer}>
          <button
            onClick={undo}
            style={styles.navButton}
            disabled={history.length === 0}
          >
            Undo
          </button>
          <button
            onClick={redo}
            style={styles.navButton}
            disabled={redoStack.length === 0}
          >
            Redo
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div style={styles.container}>
        {/* Document panel */}
        <div style={styles.docPanel}>
          {Object.entries(JSON.parse(document)).map(([key, value]) => {
            const stringValue = String(value);
            return stringValue.trim().startsWith('<div') ? (
              <div key={key} dangerouslySetInnerHTML={{ __html: value }} />
            ) : (
              <div key={key}>
                <JsonView
                  data={{ [key]: value }}
                  shouldExpandNode={allExpanded}
                  style={darkStyles}
                />
              </div>
            );
          })}
        </div>

        {/* Chat panel */}
        <div style={styles.chatSection}>
          <div style={styles.chatPanel}>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                flexWrap: "wrap",
                alignItems: "center",
                gap: 10,
                // justifyContent: "center",
              }}
            >
              <h2>Chat Messages</h2>
              <button
                onClick={resetConversation}
                style={{
                  ...styles.sendButton,
                  maxHeight: "50%",
                  marginLeft: "auto",
                }}
              >
                {" "}
                New Conversation
              </button>
            </div>
            {chat_messages.map((msg, index) => (
              <div style={{ width: "100%", marginTop: "10px" }}>
                <MessageBox
                  key={index}
                  position={msg.is_user_message ? "right" : "left"}
                  type={"text"}
                  title={
                    msg.is_user_message
                      ? "You"
                      : recipients[msg.from_id - 1].name + " Bot"
                  }
                  text={<Markdown>{msg.message}</Markdown>}
                  date={new Date(msg.creation_time)}
                />
              </div>
            ))}
          </div>
          <div style={styles.messageInputContainer}>
            <textarea
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message here..."
              style={styles.messageInput}
            />
            <select
              value={toId}
              onChange={(e) => setToId(e.target.value)}
              style={styles.recipientSelect}
            >
              <option value="">Select Recipient</option>
              {recipients.map((recipient) => (
                <option key={recipient.id} value={recipient.id}>
                  {recipient.name}
                </option>
              ))}
            </select>
            <button
              onClick={sendMessage}
              style={{
                ...styles.sendButton,
                backgroundColor: messageSending ? "#ccc" : "#007bff",
              }}
              disabled={messageSending}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  pageContainer: {
    display: "flex",
    flexDirection: "column",
    width: "100vw",
    height: "100vh",
    fontFamily: "Arial, sans-serif",
  },
  navbar: {
    height: "60px",
    backgroundColor: "#282c34",
    display: "flex",
    alignItems: "center",
    padding: "0 20px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    flexShrink: 0,
  },
  logo: {
    height: "40px",
  },
  navButtonsContainer: {
    marginLeft: "auto",
    display: "flex",
    gap: "10px",
  },
  navButton: {
    padding: "0.5rem 1rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  container: {
    display: "flex",
    flexDirection: "row",
    flex: 1,
    overflow: "hidden",
  },
  docPanel: {
    flex: 2,
    borderRight: "1px solid #ccc",
    padding: "1rem",
    overflowY: "auto",
    backgroundColor: "#f9f9f9",
  },
  chatPanel: {
    flex: 1,
    padding: "1rem",
    overflowY: "scroll",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#ffffff",
    maxHeight: "100%",
  },
  chatSection: {
    flex: 1,
    padding: "1rem",
    display: "flex",
    maxHeight: "100%",
    flexDirection: "column",
    backgroundColor: "#ffffff",
  },
  messageInputContainer: {
    marginTop: "auto",
    display: "flex",
    alignItems: "center",
  },
  messageInput: {
    flex: 1,
    padding: "0.5rem",
    marginRight: "10px",
    border: "1px solid #ccc",
    borderRadius: "4px",
  },
  recipientSelect: {
    width: "30%",
    padding: "0.5rem",
    marginRight: "10px",
    border: "1px solid #ccc",
    borderRadius: "4px",
  },
  sendButton: {
    padding: "0.5rem 1rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  loading: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    fontSize: "1.5rem",
  },
  error: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    color: "red",
    fontSize: "1.5rem",
  },
};

export default DocumentView;
