import "../ComponentStyles/LandHero.css";
import LandBg from "../assets/Images/LandBG.png";

function LandHero() {
    return (
        <div className="hero">
            <div className="leftPanel">
                <div className="mainhead">
                    <h1>Skeduler</h1>
                    <h2>Intelligent Timetabling, Solved.</h2>
                </div>

                <div className="subhead">
                    <h3>Our new scheduling platform eliminates staff conflicts, balances faculty workloads, and generates your entire department's timetable in minutes. This is the end of manual scheduling errors.</h3>
                </div>

                <div className="cta-area">
                    <button className="cta">Get Started</button>
                    <button className="cta" onClick={() => window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })}>Learn More</button>
                </div>

            </div>
            <div className="rightPanel">
                <img src={LandBg} alt="" />
            </div>
        </div>
    )
}

export default LandHero
