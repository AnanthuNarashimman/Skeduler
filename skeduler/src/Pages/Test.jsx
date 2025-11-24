import React, { useState, useEffect } from 'react';
import axios from 'axios';

import "../PageStyles/Test.css";

function Test() {
    const [data, setData] = useState(null);
    const [schedule, setSchedule] = useState(null);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState("");

    // 1. Load initial data from Flask backend when the app starts
    useEffect(() => {
        axios.get('http://localhost:5000/api/data')
            .then(res => {
                console.log("Data loaded:", res.data);
                setData(res.data);
            })
            .catch(err => {
                console.error("Error loading data:", err);
                setMsg("Error loading data from backend. Is Flask running?");
            });
    }, []);

    // 2. Handler to generate the timetable
    const handleGenerate = () => {
        setLoading(true);
        setMsg("Optimizing... This may take up to 30 seconds.");
        setSchedule(null);

        // We send the current 'data' state to the backend to ensure it uses the latest config
        axios.post('http://localhost:5000/api/generate', data)
            .then(res => {
                setLoading(false);
                if (res.data.status === 'success') {
                    setSchedule(res.data.schedule);
                    setMsg("✅ Schedule Generated Successfully!");
                } else {
                    setMsg("❌ Error: " + res.data.message);
                }
            })
            .catch(err => {
                setLoading(false);
                setMsg("❌ Server Error. Check Flask console.");
                console.error(err);
            });
    };

    if (!data) return <div className="loading-screen">Connecting to Backend...</div>;

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>Department Scheduler</h1>
                <p>Intelligent Timetabling System</p>
            </header>

            <div className="controls">
                <button
                    onClick={handleGenerate}
                    disabled={loading}
                    className={`generate-btn ${loading ? 'disabled' : ''}`}
                >
                    {loading ? "Running CP-SAT Solver..." : "Generate Timetable"}
                </button>
                <span className="status-msg">{msg}</span>
            </div>

            {/* 3. Visualization Section */}
            {schedule && (
                <div className="timetable-view">
                    {Object.keys(schedule).sort().map(className => (
                        <div key={className} className="class-card">
                            <h2 className="class-title">Class: {className}</h2>
                            <div className="grid-container">
                                {/* Header Row */}
                                <div className="grid-header-cell">Day / Period</div>
                                {[1, 2, 3, 4, 5, 6, 7].map(p => (
                                    <div key={p} className="grid-header-cell">P{p}</div>
                                ))}

                                {/* Rows for Days */}
                                {[0, 1, 2, 3, 4, 5].map(day => {
                                    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                                    const dayData = schedule[className][day.toString()] || [];
                                    return (
                                        <React.Fragment key={day}>
                                            <div className="grid-day-cell">{days[day]}</div>
                                            {dayData.map((subject, idx) => (
                                                <div key={idx} className={`grid-cell ${subject === "--- FREE ---" ? "free-cell" : "filled-cell"}`}>
                                                    {subject}
                                                </div>
                                            ))}
                                        </React.Fragment>
                                    )
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* 4. Data Verification View (Hidden when schedule is shown to keep UI clean) */}
            {!schedule && (
                <div className="data-preview">
                    <h3>Current Configuration (Loaded from server/data.json)</h3>
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default Test
