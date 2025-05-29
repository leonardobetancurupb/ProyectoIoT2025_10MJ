import "./Overview.css"
import { HiOutlineBell, HiOutlineLogout } from "react-icons/hi";
import { HiSearch } from "react-icons/hi";
import HistSensores from "../graficas/HistSensores";
import GraphReg from "../graficas/GraphReg";
import NavBar from "../navBar/NavBar";
import Notificacion from "../notCard/Notificacion";


const Overview = () => {

    //datos necesarios para la grafica historicos
    const days = ['2025-05-20', '2025-05-21', '2025-05-22', '2025-05-23', '2025-05-24'];
    const temps = [22.5, 23.1, 21.8, 22.0, 23.5];
    const hums = [55, 60, 58, 53, 57];

    //datos necesarios para las notificaciones
    const not = [
        { id: "sensor 1", temp: 23.2, hum: 87 },
        { id: "sensor 2", temp: 48.2, hum: 17 }
    ]

    //datos necesarios ultimo registro
    const ult_hum = 42.3;
    const ult_temp = 22.5;

    const handleLogOut = () =>{
        localStorage.removeItem('UserToken');
        window.location.href = '/';
    }

    return (
        <>
            <div className="ov">
                <NavBar active={"home"} />

                <div className="ov_right">
                    <div className="ho">
                        <div className="ho_search">
                            <p className="ho_title"> Overview </p>
                            <HiSearch className="ho_icon" />
                            <p className="ho_sub">Buscar...</p>
                        </div>
                        <div className="ho_not_container">
                            <div className="ho_not">
                                <HiOutlineBell className="hon_icon" />
                            </div>
                            <div   onClick={handleLogOut} className="ho_not">
                                <HiOutlineLogout className="hon_icon" />
                            </div>
                        </div>
                    </div>

                    <div className="ov_dash">
                        <div className="ovd_left">
                            <div className="ovd_main">
                                <div className="ovdm_header">
                                    <p className="ovdm_title"> Visión General de Sensores </p>
                                    <p className="ovdm_sub"> Historico promedio de todos los registros de humedad y temperatura </p>
                                </div>
                                <div className="ovdm_info">
                                    <div className="ovdm_usr">
                                        <p className="ovdmi_title">10</p>
                                        <div className="">
                                            <p className="ovdmi_sub">Usuarios</p>
                                            <p className="ovdmi_sub2">en total</p>
                                        </div>
                                    </div>
                                    <div className="ovdm_usr dg">
                                        <p className="ovdmi_title">10</p>
                                        <div className="">
                                            <p className="ovdmi_sub">Sensores</p>
                                            <p className="ovdmi_sub2">en total</p>
                                        </div>
                                    </div>
                                    <div className="ovdm_usr g">
                                        <p className="ovdmi_title">1000</p>
                                        <div className="">
                                            <p className="ovdmi_sub">Registros</p>
                                            <p className="ovdmi_sub2">en total</p>
                                        </div>
                                    </div>
                                </div>
                                <div className="ovdm_graph">
                                    <HistSensores days={days} temps={temps} hums={hums} className="hist_sensores" />
                                </div>
                            </div>

                        </div>
                        <div className="ovd_right">

                            <div className="ovdr_not">
                                <p className="ovdrn_title">Notificaciones</p>

                                {
                                    not.map(not => (
                                        <Notificacion id={not.id} temp={not.temp} hum={not.hum} />
                                    ))
                                }
                            </div>

                            <div className="ovdmb_left">
                                <p className="ovdrnh_title"> Ultimo registro de humedad </p>
                                <div className="ovdmb_graph">
                                    <GraphReg label={"Humedad"} value={ult_hum} color={"#60a5fa"} />
                                </div>
                            </div>

                            <div className="ovdmb_right">
                                <p className="ovdrnh_title"> Ultimo registro de temperatura </p>
                                <div className="ovdmb_graph">
                                    <GraphReg label={"Temperatura"} value={ult_temp} color={"#FEF100"} />
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

            </div>
        </>
    )
}

export default Overview