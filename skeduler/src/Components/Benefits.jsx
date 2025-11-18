import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import "../ComponentStyles/Benefits.css";

import BenefitImage from "../assets/Images/Benefits.png";

gsap.registerPlugin(ScrollTrigger);

function Benefits() {
    const sectionRef = useRef(null);
    const headlineRef = useRef(null);
    const imageRef = useRef(null);
    const [currentBenefit, setCurrentBenefit] = useState(0);
    const benefitRef = useRef(null);

    const benefits = [
        {
            category: "For the HOD & Admin",
            items: [
                {
                    title: "Save Weeks of Time",
                    description: "Generate the entire department's schedule in minutes, not weeks."
                },
                {
                    title: "100% Error-Free",
                    description: "Eliminates all human error from staff conflicts and rule violations."
                },
                {
                    title: "Instant Adaptability",
                    description: "Need to make a change? Add a new constraint and get a new, fully optimized schedule in seconds."
                }
            ]
        },
        {
            category: "For the Faculty",
            items: [
                {
                    title: "Balanced & Fair Workload",
                    description: "The optimizer's first goal is to assign subjects fairly, ensuring no staff member is overburdened."
                },
                {
                    title: "A Reliable Schedule",
                    description: "A stable, conflict-free timetable from day one of the semester."
                }
            ]
        },
        {
            category: "For the Students",
            items: [
                {
                    title: "A Better Learning Experience",
                    description: "A balanced schedule that intelligently spreads out labs, lectures, and special periods throughout the week."
                }
            ]
        }
    ];

    // Flatten all benefits for rotation
    const allBenefits = benefits.flatMap((benefit, catIndex) =>
        benefit.items.map((item, itemIndex) => ({
            ...item,
            category: benefit.category,
            key: `${catIndex}-${itemIndex}`
        }))
    );

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

            // Image animation
            gsap.fromTo(
                imageRef.current,
                { opacity: 0, x: 100, scale: 0.95 },
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
        }, sectionRef);

        return () => ctx.revert();
    }, []);

    // Auto-rotate benefits with bouncy animation
    useEffect(() => {
        const interval = setInterval(() => {
            if (benefitRef.current) {
                // Bouncy exit animation
                gsap.to(benefitRef.current, {
                    x: -100,
                    opacity: 0,
                    duration: 0.5,
                    ease: "back.in(1.7)",
                    onComplete: () => {
                        setCurrentBenefit((prev) => (prev + 1) % allBenefits.length);
                        // Bouncy enter animation
                        gsap.fromTo(
                            benefitRef.current,
                            { x: 100, opacity: 0 },
                            {
                                x: 0,
                                opacity: 1,
                                duration: 0.6,
                                ease: "back.out(1.7)"
                            }
                        );
                    }
                });
            }
        }, 4000); // Change every 4 seconds

        return () => clearInterval(interval);
    }, [allBenefits.length]);

    return (
        <section className="benefits-section" id="benefits" ref={sectionRef}>
            <div className="benefits-container">
                <h2 className="benefits-headline" ref={headlineRef}>
                    What This Means for Our Department
                </h2>

                <div className="benefits-content">
                    <div className="benefits-left">
                        <div className="benefit-display" ref={benefitRef}>
                            <div className="benefit-category">
                                {allBenefits[currentBenefit].category}
                            </div>
                            <h3 className="benefit-title">
                                {allBenefits[currentBenefit].title}
                            </h3>
                            <p className="benefit-description">
                                {allBenefits[currentBenefit].description}
                            </p>
                        </div>

                        <div className="benefit-indicators">
                            {allBenefits.map((_, index) => (
                                <div
                                    key={index}
                                    className={`indicator ${index === currentBenefit ? 'active' : ''}`}
                                    onClick={() => setCurrentBenefit(index)}
                                />
                            ))}
                        </div>
                    </div>

                    <div className="benefits-right" ref={imageRef}>
                        <img src={BenefitImage} alt="Benefits illustration" className="benefits-image" />
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Benefits;
