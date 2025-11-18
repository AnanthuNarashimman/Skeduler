import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import "../ComponentStyles/Solution.css";
import SolutionImage from "../assets/Images/Solution.png";

gsap.registerPlugin(ScrollTrigger);

function Solution() {
    const sectionRef = useRef(null);
    const headlineRef = useRef(null);
    const contentRef = useRef(null);
    const imageRef = useRef(null);
    const paragraphsRef = useRef([]);

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

            // Image animation (from left since it's on the left side)
            gsap.fromTo(imageRef.current,
                { opacity: 0, x: -100, scale: 0.9 },
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

            // Content paragraphs stagger animation
            paragraphsRef.current.forEach((paragraph, index) => {
                if (paragraph) {
                    gsap.fromTo(paragraph,
                        { opacity: 0, y: 30 },
                        {
                            scrollTrigger: {
                                trigger: paragraph,
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

    const setParagraphRef = (index) => (el) => {
        if (el) paragraphsRef.current[index] = el;
    };

    return (
        <section className="solution-section" id="solution" ref={sectionRef}>
            <div className="solution-container">
                <div className="solution-image" ref={imageRef}>
                    <img src={SolutionImage} alt="Skeduler intelligent scheduling solution" />
                </div>

                <div className="solution-content">
                    <h2 className="solution-headline" ref={headlineRef}>
                        Introducing the Skeduler Scheduler
                    </h2>

                    <div className="solution-description" ref={contentRef}>
                        <p ref={setParagraphRef(0)}>
                            We've replaced the manual guesswork with a powerful, intelligent scheduling engine.
                        </p>

                        <p ref={setParagraphRef(1)}>
                            This platform isn't just a digital calendar; it's a dedicated optimization tool built specifically for our department's complex needs. It mathematically analyzes every single constraint—all 7+ classes, all 30+ staff members, all labs, and all special periods—at the same time.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Solution;
