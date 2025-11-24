import Navbar from "../Components/Navbar";
import LandHero from "../Components/LandHero";
import Problem from "../Components/Problem";
import Solution from "../Components/Solution";
import Features from "../Components/Features";
import Benefits from "../Components/Benefits";
import CTA from "../Components/CTA";
import Footer from "../Components/Footer";


import "../PageStyles/LandingPage.css";

import Logo from "../assets/Images/Logo.png";

function LandingPage() {
    const items = [
        {
            label: "About the Project",
            bgColor: "#0D0716",
            textColor: "#fff",
            links: [
                { label: "The Problem", ariaLabel: "About Problem", href: "#problem" },
                { label: "The Solution", ariaLabel: "About Solution", href: "#solution" }
            ]
        },
        {
            label: "How It Works",
            bgColor: "#170D27",
            textColor: "#fff",
            links: [
                { label: "Core Features", ariaLabel: "Code Features", href: "#features" },
                { label: "Benefits", ariaLabel: "About Benefits", href: "#benefits" }
            ]
        },
        {
            label: "Portal Access",
            bgColor: "#6ba3d8",
            textColor: "#fff",
            links: [
                { label: "Teacher Login", ariaLabel: "Teacher Login Portal", href: "/teacher/login" },
                { label: "Try Admin Demo", ariaLabel: "Try Admin Demo", href: "/admin/dashboard" }
            ]
        }
    ];


    return (
        <div className="landing-page">
            <Navbar
                logo={Logo}
                logoAlt="Company Logo"
                items={items}
                baseColor="#fff"
                menuColor="#000"
                buttonBgColor="#111"
                buttonTextColor="#fff"
                ease="power3.out" />

            <LandHero />

            <Problem />

            <Solution />

            <Features />

            <Benefits />

            <CTA />

            <Footer />
        </div>
    )
}

export default LandingPage
