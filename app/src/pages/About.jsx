import React from 'react';
import Navbar from '../components/Navbar';
import paths from '../utils/paths';

export default function About() {
    return (
        <div>
            {/* Include the Navbar */}
            <Navbar />

            {/* About page content */}
            <div className="about-container">
                <h1 className="about-title">About Us</h1>

                <p className="about-text">
                    Our project is a rehabilitation program designed to help individuals track and reclaim their range of motion (ROM) in injured joints. Whether you’re recovering from a shoulder dislocation or any injury resulting in reduced ROM, this program is here to guide you through your recovery journey.
                </p>

                {/* Containers for additional information */}
                <div className="about-panels">
                    {/* First Panel */}
                    <div className="about-panel">
                        <h3 className="panel-title"><strong>Features</strong></h3>
                        <p className="panel-text">
                            <strong>ROM Tracking</strong>: Uses OpenCV to calculate the angle and range of motion of your joint daily.<br /><br />
                            <strong>AI Recommendations</strong>: A trained physiotherapist AI suggests recovery programs based on your progress.<br /><br />
                            <strong>Streamlit Data Visualization</strong>: Displays clear and interactive graphs to track your rehabilitation journey.<br /><br />
                            <strong>User Logins and Cloud Storage</strong>: With a secure login system and MongoDB database, individual users can create accounts, save their data, and access it across devices.
                        </p>
                    </div>

                    {/* Second Panel */}
                    <div className="about-panel">
                        <h3 className="panel-title"><strong>Our Technology</strong></h3>
                        <p className="panel-text">
                            <strong>React</strong>: Frontend framework to create a responsive and user-friendly interface.<br /><br />
                            <strong>Streamlit</strong>: For plotting data and visualizing the recovery journey.<br /><br />
                            <strong>OpenCV</strong>: To track and calculate the ROM using camera input.<br /><br />
                            <strong>Flask</strong>: Backend server to manage data flow and user authentication.<br /><br />
                            <strong>MongoDB</strong>: Cloud database to securely store user information and progress.
                        </p>
                    </div>
                </div>

                <div className="about-section">
                    <h1 className="about-title">How It Works</h1>

                    <p className="about-text how-it-works">
                        Using cutting-edge computer vision technology with OpenCV, we track the daily angle of movement in your injured joint. For example, in the case of a shoulder dislocation, the program measures how far up your arm can move daily, recording your progress in real time.<br /><br />
                        The data collected is then analyzed by a trained Physiotherapist AI, which recommends a personalized rehabilitation program tailored to your recovery. Every day, you test your maximum ROM to monitor the effectiveness of the suggested exercises.<br /><br />
                        Through Streamlit, we visualize this data, allowing you to see how much of your ROM you’ve reclaimed over time in intuitive and interactive graphs.
                    </p>
                </div>

                {/* Logo Section */}
                <div className="logo-container">
                    <div className="logo">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="400" height="300">
                            <g id="Layer1">
                                {paths.map((path) => (
                                    <path key={path.id} id={path.id} fillRule="evenodd" className="s0" d={path.d} />
                                ))}
                            </g>
                        </svg>
                    </div>
                    <div className="logo-text">Qmove</div>
                </div>
            </div>
        </div>
    );
}
