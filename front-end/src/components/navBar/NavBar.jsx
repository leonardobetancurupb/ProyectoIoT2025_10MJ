import "./NavBar.css";
import { HiHome } from "react-icons/hi";
import { HiServer } from "react-icons/hi";
import esc_upb from "../../assets/esc_upb.png";
import usr from "../../assets/usr.jpg";

const NavBar = ( {active} ) =>{

    return (
        <>
            <div className="ov_left">
                <div className="ov_menu">
                    <div className="ov_logo">
                        <a href="/">  <img src={esc_upb} alt="upb_logo" className="ov_icon_size"/> </a>
                    </div>

                    <div className="ovm_opcs">
                        <a href="/overview" className= {active == 'home' ? 'ovm_opc_active' : 'ovm_opc'}> <HiHome className="ovm_opc_icon"/> </a> 
                        <a href="/sensor" className={active == 'sensores' ? 'ovm_opc_active' : 'ovm_opc'}> <HiServer className="ovm_opc_icon"/> </a> 
                    </div>
                    <div className="ovm_usr">
                        <img src={usr} alt="" className="ov_user"/>
                    </div>
                </div>
            </div>            
        </>
    )
}

export default NavBar