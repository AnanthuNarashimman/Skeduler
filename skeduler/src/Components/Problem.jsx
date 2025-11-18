import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import "../ComponentStyles/Problem.css";

import ProblemImage from "../assets/Images/Problem.jpg";
import SolutionImage from "../assets/Images/Solution.png";

gsap.registerPlugin(ScrollTrigger);

function Problem() {
    const sectionRef = useRef(null);
    const headlineRef = useRef(null);
    const contentRef = useRef(null);
    const imageRef = useRef(null);
    const pointsRef = useRef([]);

    useEffect(() => {
        const ctx = gsap.context(() => {
            // Headline animation
            gsap.fromTo(headlineRef.current, 
                { opacity: 0, y: 50 },
                {
                    scrollTrigger: {
                        trigger: sectionRef.current,
                        start: "top 80%",
                        end: "top 50%",
                        scrub: 1,
                    },
                    opacity: 1,
                    y: 0,
                }
            );

            // Image animation
            gsap.fromTo(imageRef.current,
                { opacity: 0, x: 100, scale: 0.9 },
                {
                    scrollTrigger: {
                        trigger: sectionRef.current,
                        start: "top 70%",
                        end: "top 40%",
                        scrub: 1,
                    },
                    opacity: 1,
                    x: 0,
                    scale: 1,
                }
            );

            // Content points stagger animation
            pointsRef.current.forEach((point, index) => {
                if (point) {
                    gsap.fromTo(point,
                        { opacity: 0, y: 30 },
                        {
                            scrollTrigger: {
                                trigger: point,
                                start: "top 85%",
                                end: "top 55%",
                                scrub: 1,
                            },
                            opacity: 1,
                            y: 0,
                        }
                    );
                }
            });
        }, sectionRef);

        return () => ctx.revert();
    }, []);

    const setPointRef = (index) => (el) => {
        if (el) pointsRef.current[index] = el;
    };

    return (
        <section className="problem-section" id="problem" ref={sectionRef}>
            <div className="problem-container">
                <div className="problem-content">
                    <h2 className="problem-headline" ref={headlineRef}>
                        The Manual Scheduling Nightmare
                    </h2>

                    <div className="problem-points" ref={contentRef}>
                        <div className="problem-point" ref={setPointRef(0)}>
                            <h3>Weeks of Wasted Effort</h3>
                            <p>Hours and days spent in spreadsheet cells, trying to manually cross-reference staff, classes, and rooms.</p>
                        </div>

                        <div className="problem-point" ref={setPointRef(1)}>
                            <h3>Hidden Staff Conflicts</h3>
                            <p>It's almost impossible to manually guarantee that a single staff member (e.g., one teaching a lab and a lecture) isn't accidentally scheduled in two places at once.</p>
                        </div>

                        <div className="problem-point" ref={setPointRef(2)}>
                            <h3>Unbalanced Schedules</h3>
                            <p>Students face unbalanced days with all labs clustered together, while staff are left with inefficient gaps and unfair workloads.</p>
                        </div>
                    </div>
                </div>

                <div className="problem-image" ref={imageRef}>
                    <img src={ProblemImage} alt="Manual scheduling problems illustration" />
                </div>
            </div>
        </section>
    );
}

export default Problem;
