import React, { useState } from 'react';

const UserInputForm = ({ onNext }) => {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [insurance, setInsurance] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onNext({ age, gender, insurance });
    };

    return (
        <div className="user-input-form">
            <h2>Personal Information</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Age:</label>
                    <input
                        type="number"
                        value={age}
                        onChange={(e) => setAge(e.target.value)}
                    />
                </div>
                <div>
                    <label>Gender:</label>
                    <select value={gender} onChange={(e) => setGender(e.target.value)}>
                        <option value="">Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div>
                    <label>Insurance Provider:</label>
                    <input
                        type="text"
                        value={insurance}
                        onChange={(e) => setInsurance(e.target.value)}
                    />
                </div>
                <button type="submit">Next</button>
            </form>
        </div>
    );
};

export default UserInputForm;
