import React, { useState } from 'react';

const SymptomsInput = ({ onNext }) => {
    const [symptoms, setSymptoms] = useState('');
    const [duration, setDuration] = useState('');
    const [severity, setSeverity] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onNext({ symptoms, duration, severity });
    };

    return (
        <div className="symptoms-input">
            <h2>Describe Your Symptoms</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Symptoms:</label>
                    <textarea
                        value={symptoms}
                        onChange={(e) => setSymptoms(e.target.value)}
                    />
                </div>
                <div>
                    <label>Duration (in days):</label>
                    <input
                        type="number"
                        value={duration}
                        onChange={(e) => setDuration(e.target.value)}
                    />
                </div>
                <div>
                    <label>Severity (1-10):</label>
                    <input
                        type="number"
                        value={severity}
                        onChange={(e) => setSeverity(e.target.value)}
                    />
                </div>
                <button type="submit">Next</button>
            </form>
        </div>
    );
};

export default SymptomsInput;
