import React from "react";
import "./LandingPage.css";
import upb from "../../assets/logo_upb.png";
import esc_upb from "../../assets/esc_upb.png";
import { HiArrowNarrowRight  } from "react-icons/hi";
import { Link } from "react-router-dom";
const LandingPage = () =>{

    const token = localStorage.getItem('UserToken');
    
    return(
        <>
            <div className="lp">
                <div className="h_lp">
                    <img src={upb} alt="upb_logo" className="h_logo" />
                    <div className="h_nl">
                        <a href="https://www.upb.edu.co/" type="_blank" className="h_l"> ABOUT UPB </a>
                        <a href="https://github.com/juanVolkmar/SensoresIoT" type="_blank" className="h_l"> GITHUB </a>
                    </div>
                    <Link to={token ? '/overview' : '/login'} className="h_l btn"> GET STARTED </Link>

                </div>

                <div className="t_lp">
                    <div className="t_top">
                        <p className="tt_text tt_space"> ALL YOUR </p>
                        <HiArrowNarrowRight className="tt_arrow btn2"/>
                        <p className="tt_text"> CRAZY IOT </p>
                    </div>
                    <div className="t_bottom">
                        <Link to="/sensor" className="h_l btn tt_space2"> Explore the sensors </Link>
                        <p className="tt_text"> DEVICES ARE IN HERE </p>
                    </div>
                </div>

                <div className="f_lp">
                    <div className="b_box">
                        <p className="bb_title"> Final </p>
                        <p className="bb_sub"> Second IoT exam </p>
                        <p className="bb_note"> Leonardo Betancur Agudelo </p>
                    </div>
                    <div className="s_box">
                        <div className="s_team">
                            <div className="">
                                <p className="sb_name"> Maria Paula Florez Vargas </p>
                                <p className="sb_note"> Ingenieria en Sistemas e Informatica </p>
                            </div>
                            <div className="">
                                <p className="sb_name"> Jose Manuel Garces Molina </p>
                                <p className="sb_note"> Ingenieria en Sistemas e Informatica </p>
                            </div>
                        </div>

                        <div className="s_team">
                            <div className="">
                                <p className="sb_name"> Juan Manuel Volkmar P. </p>
                                <p className="sb_note"> Ingenieria en Sistemas e Informatica </p>
                            </div>
                            <div className="">
                                <p className="sb_name"> Santiago Restrepo Chalarca </p>
                                <p className="sb_note"> Ingenieria en Sistemas e Informatica </p>
                            </div>
                        </div>

                        <p className="bb_note center"> Equipo Paw Patrol </p>
                    </div>

                    <div className="b_box2">
                        <p className="bb_title2"> Tradition <br></br> of excellent <br></br> quality </p>
                        <p className="bb_note"> Universidad Pontificia Bolivariana </p>
                    </div>
                </div>

            </div>
        </>
    )
}

export default LandingPage