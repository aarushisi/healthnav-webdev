import React from 'react';

const DoctorResults = ({ recommendations }) => {
    return (
        <div className="doctor-results">
            <h2>Doctor Recommendations</h2>
            {recommendations.length === 0 ? (
                <p>No doctors found for your criteria.</p>
            ) : (
                <ul>
                    {recommendations.map((doctor, index) => (
                        <li key={index}>
                            <p>{doctor.name}</p>
                            <p>{doctor.specialty}</p>
                            <p>{doctor.location}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DoctorResults;
