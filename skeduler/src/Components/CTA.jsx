import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useNavigate } from 'react-router-dom';
import { FaArrowRight, FaRocket } from "react-icons/fa";
import "../ComponentStyles/CTA.css";

gsap.registerPlugin(ScrollTrigger);

function CTA() {
    const sectionRef = useRef(null);
    const contentRef = useRef(null);
    const buttonsRef = useRef(null);
    const navigate = useNavigate();

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
                    <h2 className="cta-headline">Experience Intelligent Scheduling</h2>
                    <p className="cta-description">
                        Try our demo dashboard to see how easy it is to manage your department's data and generate conflict-free timetables.
                    </p>
                </div>

                <div className="cta-buttons" ref={buttonsRef}>
                    <button className="cta-button primary" onClick={() => navigate('/admin/dashboard')}>
                        <FaRocket className="button-icon" />
                        Try Demo
                        <FaArrowRight className="button-arrow" />
                    </button>
                </div>
            </div>
        </section>
    );
}

export default CTA;
