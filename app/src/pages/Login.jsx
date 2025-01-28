import { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap"; //move pieces of logo
import paths from '../utils/paths';
export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        // Define the timeline for the animation
        const tl = gsap.timeline();

        // Initial animation: Move pieces apart at start
        paths.forEach((path, index) => {
            gsap.set(`#${path.id}`, {
                x: index % 2 === 0 ? -200 : 200,
                y: index % 3 === 0 ? -200 : 200,
                opacity: 0,
            });
        });

        // Assemble animation: Move pieces together and fade in
        const assembleTimeline = gsap.timeline();

        // Add animations for each shape
        paths.forEach((path, index) => {
            assembleTimeline.to(
                `#${path.id}`,
                {
                    x: 0,
                    y: 0,
                    opacity: 1,
                    duration: 2,
                    ease: "power2.out",
                },
                `-=${index === 0 ? 0 : 1.8}` // Overlap animations
            );
        });

         assembleTimeline.eventCallback("onComplete", () => {
            gsap.utils.toArray("path").forEach((shape) => {
                gsap.to(shape, {
                x: `random(-5, 5)`, // Random horizontal movement
                y: `random(-8, 8)`, // Random vertical movement
                duration: `random(3, 6)`, // Random duration between 3 and 6 seconds
                repeat: -1, // Infinite loop
                yoyo: true, // Reverse the motion
                ease: "power1.inOut", // Smooth easing for natural movement
                });
            });
        })
    }, []);

  const login = () => {
    if (email === "" && password === "") {
      alert("Invalid email or password");
    } else {
      console.log("Login successful!");
      navigate("/dashboard"); // Redirect to the dashboard
    }
  };

    return (
        <div className="login-container">
            {/* Display the logo using the public folder */}
            <div className="logo">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 500 500"
                    width="400"
                    height="300"
                >
                    <g id="Layer1">
                        {paths.map((path) => (
                            <path
                                key={path.id}
                                id={path.id}
                                fillRule="evenodd"
                                className="s0"
                                d={path.d}
                            />
                        ))}
                    </g>
                </svg>
                <div style={{ fontFamily: "'Impact', sans-serif", fontSize: "6rem", marginTop: "-35px"}}>
                Qmove
                </div>
            </div>

            <div className="login" style={{ textAlign: "center", marginTop: "40px" }}>
                <h1>Login</h1>
                <input
                    className="login-input"
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    className="login-input"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button
                    onClick={login}
                    className="login-button"
                >
                        Log in
                </button>
            </div>
        </div>
    );
}
