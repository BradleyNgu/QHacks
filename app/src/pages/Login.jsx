import { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap"; //move pieces of logo

export default function Login() {

    const paths = [
        { id: "shape1", d: "m10 106l14 68 16-32z" },
        { id: "shape2", d: "m45 159l-10 12-3 8 27 1z" },
        { id: "shape3", d: "m26 185l-19 44 38-17 57 13-32-27-10-13z" },
        { id: "shape4", d: "m5 117l-2 105 18-40z" },
        { id: "shape5", d: "m4 236l42-16 66 12-25 42 15 60-60-37-36-34z" },
        { id: "shape6", d: "m116 235l-20 37 59 18-11-31z" },
        { id: "shape7", d: "m152 265l20 48 36-13-2-50z" },
        { id: "shape8", d: "m94 277l16 62 48 21-3-63z" },
        { id: "shape9", d: "m161 300l4 58 9.5-24.7z" },
        { id: "shape10", d: "m174 353l7-20 20 8z" },
        { id: "shape11", d: "m209 306l-2 33-29-12-2-10z" },
        { id: "shape12", d: "m356 185l-60 32 38 19-5 38 60-42 9-39z" },
        { id: "shape13", d: "m214 248l75-27 35 18-82 27z" },
        { id: "shape14", d: "m214 260l50 26-47 15z" },
        { id: "shape15", d: "m253 269l43 27 28-48z" },
        { id: "shape16", d: "m308 290l15-11 4-23z" },
        { id: "shape17", d: "m219 310v25l72-32-16-10z" },
        { id: "shape18", d: "m359 179l29 3-18-56z" },
        { id: "shape19", d: "m372 75l19 25-18 1z" },
        { id: "shape20", d: "m373 106l17-1 3 28-2 43-19-55z" },
        { id: "shape21", d: "m401 130l65 47-32 25z" },
        { id: "shape22", d: "m405 127l54 39-8-31-27-21z" },
        { id: "shape23", d: "m397 141l5-1 27 65-29 19 8-40-12-4z" }
    ];

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
