import { FaEnvelope, FaLinkedin } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import "../ComponentStyles/Footer.css";

function Footer() {
    const teamMembers = [
        {
            name: "Ananthu",
            gmail: "ananthu@example.com",
            linkedin: "https://linkedin.com/in/ananthu",
            twitter: "https://twitter.com/ananthu"
        },
        {
            name: "Aditya",
            gmail: "aditya@example.com",
            linkedin: "https://linkedin.com/in/aditya",
            twitter: "https://twitter.com/aditya"
        },
        {
            name: "Balamurugan",
            gmail: "balamurugan@example.com",
            linkedin: "https://linkedin.com/in/balamurugan",
            twitter: "https://twitter.com/balamurugan"
        }
    ];

    return (
        <footer className="footer" id="footer">
            <div className="footer-container">
                <div className="footer-top">
                    <div className="footer-info">
                        <h3 className="footer-title">Skeduler</h3>
                        <p className="footer-subtitle">Intelligent Timetabling, Solved.</p>
                    </div>

                    <div className="footer-team">
                        <h4 className="team-heading">Project Team</h4>
                        <div className="team-members">
                            {teamMembers.map((member, index) => (
                                <div key={index} className="team-member">
                                    <span className="member-name">{member.name}</span>
                                    <div className="member-socials">
                                        <a
                                            href={`mailto:${member.gmail}`}
                                            className="social-link"
                                            aria-label={`Email ${member.name}`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <FaEnvelope />
                                        </a>
                                        <a
                                            href={member.linkedin}
                                            className="social-link"
                                            aria-label={`${member.name}'s LinkedIn`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <FaLinkedin />
                                        </a>
                                        <a
                                            href={member.twitter}
                                            className="social-link"
                                            aria-label={`${member.name}'s Twitter`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <FaXTwitter />
                                        </a>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="footer-divider"></div>

                <div className="footer-bottom">
                    <p className="footer-copyright">
                        © 2025 KSR College of Engineering | Department of Computer Science & Engineering
                    </p>
                    <p className="footer-credit">
                        A Project by Ananthu, Aditya, Balamurugan
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
