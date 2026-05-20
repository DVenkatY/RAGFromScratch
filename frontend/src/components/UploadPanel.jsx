import React, { useState } from 'react';
import { api } from '../services/api';

const UploadPanel = ({ onTableReady }) => {
    const [file, setFile] = useState(null);
    const [isIngesting, setIsIngesting] = useState(false);
    const [progress, setProgress] = useState(0);
    const [metrics, setMetrics] = useState(null);
    const [uploadMessage, setUploadMessage] = useState(null);

    const handleFileUpload = (e) => {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
            setProgress(0);
            setMetrics(null);
            setUploadMessage(null);
        }
    };

    const handleIngest = async () => {
        if (!file) return;

        setIsIngesting(true);
        setProgress(5);
        setMetrics(null);
        setUploadMessage(null);

        const progressInterval = setInterval(() => {
            setProgress((prev) => (prev >= 90 ? 90 : prev + 5));
        }, 400);

        try {
            const result = await api.ingestDocument(file);
            clearInterval(progressInterval);

            if (result.status === "exists") {
                setProgress(0);
                onTableReady(result.table_name);
                setUploadMessage({ type: "warning", text: `Ingest skipped: Table for "${file.name}" already exists.` });
            } else {
                setProgress(100);
                onTableReady(result.table_name);
                if (result.metrics) setMetrics(result.metrics);
                setUploadMessage({ type: "success", text: `Ingest complete! ${result.chunks_created} chunks generated.` });
            }
        } catch (error) {
            clearInterval(progressInterval);
            setProgress(0);
            setUploadMessage({ type: "error", text: `Failed: ${error.message}` });
        } finally {
            setIsIngesting(false);
        }
    };

    return (
        <div className="w-80 bg-white p-4 shadow-lg flex flex-col justify-between overflow-y-auto">
            <div>
                <h3 className="text-lg font-semibold mb-4">Upload File</h3>

                {/* File Upload Area */}
                <div className="mb-4">
                    <label htmlFor="file-upload" className="block w-full border-2 border-dashed border-gray-300 rounded-lg p-3 text-center cursor-pointer bg-gray-50 hover:bg-gray-100 transition text-sm text-gray-600">
                        {file ? "Change File" : "Select a document..."}
                    </label>
                    <input id="file-upload" type="file" onChange={handleFileUpload} className="hidden" accept=".pdf" />
                    {file && <p className="mt-2 text-xs text-gray-500 truncate">Selected: <strong>{file.name}</strong></p>}
                </div>

                {/* Progress Bar */}
                {progress > 0 && (
                    <div className="mb-4">
                        <div className="flex justify-between text-xs font-semibold text-blue-600 mb-1">
                            <span>{progress === 100 ? "Completed" : "Ingesting data..."}</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out" style={{ width: `${progress}%` }}></div>
                        </div>
                    </div>
                )}

                {/* System Messages */}
                {uploadMessage && (
                    <div className={`mb-4 p-3 rounded-lg text-sm border ${
                        uploadMessage.type === "success" ? "bg-green-50 text-green-700 border-green-200" :
                        uploadMessage.type === "warning" ? "bg-yellow-50 text-yellow-700 border-yellow-200" :
                        "bg-red-50 text-red-700 border-red-200"
                    }`}>
                        {uploadMessage.text}
                    </div>
                )}

                {/* Metrics */}
                {metrics && (
                    <div className="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-700 font-mono shadow-inner">
                        <p className="mb-1 text-gray-500 font-sans font-semibold uppercase tracking-wider text-[10px]">Performance Metrics</p>
                        <p className="mb-1">Chunking: <span className="font-semibold text-gray-900">{metrics.chunking_seconds}s</span></p>
                        <p className="mb-1">Embedding: <span className="font-semibold text-gray-900">{metrics.embedding_seconds}s</span></p>
                        <p className="mb-1">DB Upload: <span className="font-semibold text-gray-900">{metrics.database_upload_seconds}s</span></p>
                        <div className="mt-2 pt-2 border-t border-gray-300 font-bold text-blue-700">Total: {metrics.total_processing_seconds}s</div>
                    </div>
                )}
            </div>

            {/* Submit Button */}
            <div className="pt-4 mt-auto border-t">
                <button
                    onClick={handleIngest}
                    disabled={isIngesting || !file}
                    className={`w-full text-white py-2 rounded-xl font-medium transition ${
                        isIngesting || !file ? "bg-gray-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
                    }`}
                >
                    {isIngesting ? "Processing Chunks..." : "Ingest Data"}
                </button>
            </div>
        </div>
    );
};

export default UploadPanel;