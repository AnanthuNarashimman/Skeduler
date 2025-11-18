import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { FaArrowRight, FaUserShield } from "react-icons/fa";
import "../ComponentStyles/CTA.css";

gsap.registerPlugin(ScrollTrigger);

function CTA() {
    const sectionRef = useRef(null);
    const contentRef = useRef(null);
    const buttonsRef = useRef(null);

    useEffect(() => {
        const ctx = gsap.context(() => {
            // Content animation
            gsap.fromTo(
                contentRef.current,
                { opacity: 0, y: 50 },
                {
                    scrollTrigger: {
                        trigger: sectionRef.current,
                        start: "top 75%",
                        end: "top 45%",
                        scrub: 1,
                    },
                    opacity: 1,
                    y: 0,
                }
            );

            // Buttons animation
            gsap.fromTo(
                buttonsRef.current,
                { opacity: 0, y: 30 },
                {
                    scrollTrigger: {
                        trigger: sectionRef.current,
                        start: "top 70%",
                        end: "top 40%",
                        scrub: 1,
                    },
                    opacity: 1,
                    y: 0,
                }
            );
        }, sectionRef);

        return () => ctx.revert();
    }, []);

    return (
        <section className="cta-section" ref={sectionRef}>
            <div className="cta-container">
                <div className="cta-content" ref={contentRef}>
                    <h2 className="cta-headline">Get Started with Intelligent Scheduling</h2>
                    <p className="cta-description">
                        Log in to the admin panel to manage your department's data and generate your first conflict-free timetable.
                    </p>
                </div>

                <div className="cta-buttons" ref={buttonsRef}>
                    <button className="cta-button primary">
                        <FaUserShield className="button-icon" />
                        Admin Login
                        <FaArrowRight className="button-arrow" />
                    </button>
                    <button className="cta-button secondary">
                        Login
                        <FaArrowRight className="button-arrow" />
                    </button>
                </div>
            </div>
        </section>
    );
}

export default CTA;
