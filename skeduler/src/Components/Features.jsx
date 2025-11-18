import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { FaCheckCircle, FaCogs, FaFlask, FaBookOpen, FaChartLine, FaBolt } from "react-icons/fa";
import "../ComponentStyles/Features.css";

gsap.registerPlugin(ScrollTrigger);

function Features() {
    const sectionRef = useRef(null);
    const headlineRef = useRef(null);
    const cardsRef = useRef([]);

    useEffect(() => {
        const ctx = gsap.context(() => {
            // Headline animation
            gsap.fromTo(
                headlineRef.current,
                { opacity: 0, y: 60 },
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

            // Cards stagger animation
            cardsRef.current.forEach((card, index) => {
                if (card) {
                    gsap.fromTo(
                        card,
                        { opacity: 0, y: 50, scale: 0.95 },
                        {
                            scrollTrigger: {
                                trigger: card,
                                start: "top 85%",
                                end: "top 55%",
                                scrub: 1,
                            },
                            opacity: 1,
                            y: 0,
                            scale: 1,
                        }
                    );
                }
            });
        }, sectionRef);

        return () => ctx.revert();
    }, []);

    const setCardRef = (index) => (el) => {
        if (el) cardsRef.current[index] = el;
    };

    const features = [
        {
            title: "Guaranteed Conflict-Free",
            description: "Our core logic ensures no staff member is ever double-booked, and no class is scheduled for two subjects at once. Period.",
            icon: <FaCheckCircle />
        },
        {
            title: "Multi-Class, Multi-Staff Engine",
            description: "Simultaneously generates optimized schedules for all classes in the department (III Sem, V Sem, VII Sem) at once, respecting the unique constraints of each.",
            icon: <FaCogs />
        },
        {
            title: "Intelligent Lab & Tutorial Scheduling",
            description: "Automatically places 3-period labs and 2-period tutorials in their correct, consecutive blocks, respecting all valid start times.",
            icon: <FaFlask />
        },
        {
            title: "Smart Elective Grouping",
            description: "Understands that electives (like 'BI / ASD') must be scheduled at the same time and handles the complex staff assignments for each automatically.",
            icon: <FaBookOpen />
        },
        {
            title: "Dynamic Period Calculation",
            description: "No more impossible schedules. The engine intelligently calculates the period distribution for each class to ensure the total periods always equal the 42 available slots.",
            icon: <FaChartLine />
        },
        {
            title: "Custom Rule Support",
            description: "Easily enforces all our department's specific rules: 'No labs on Saturday,' 'At most one lab session per class, per day,' 'This subject must be scheduled at this exact time,' and many more...",
            icon: <FaBolt />
        }
    ];

    return (
        <section className="features-section" id="features" ref={sectionRef}>
            <div className="features-container">
                <h2 className="features-headline" ref={headlineRef}>
                    A Complete Solution for Our Department
                </h2>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <div
                            key={index}
                            className="feature-card"
                            ref={setCardRef(index)}
                        >
                            <div className="feature-icon">{feature.icon}</div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-description">{feature.description}</p>
                            <div className="feature-glow"></div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

export default Features;
