import React, { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ChatWindow from "./components/ChatWindow";

const App = () => {
    // This state connects the Upload panel to the Chat window
    const [activeTableName, setActiveTableName] = useState("");

    return (
        <div className="h-screen flex bg-gray-100">
            {/* Left Panel */}
            <UploadPanel onTableReady={(tableName) => setActiveTableName(tableName)} />

            {/* Right Panel */}
            <ChatWindow tableName={activeTableName} />
        </div>
    );
};

export default App;