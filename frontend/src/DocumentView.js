import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

/**
 * A component that fetches and displays:
 * 1. The document (HTML) content.
 * 2. The list of chat messages.
 */
function DocumentView() {
  const { documentId } = useParams();
  const [docData, setDocData] = useState(null);
  const [loading, setLoading] = useState(true);
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
        <div dangerouslySetInnerHTML={{ __html: document }} />
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
