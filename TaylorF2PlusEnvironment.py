import numpy as np
import pycbc.waveform
# import matplotlib.pyplot as plt
from pycbc.types import FrequencySeries
from pycbc.waveform import get_fd_waveform
# from numpy import random
# from scipy import integrate


# 基本常数(后面改为调用自带的基本常数，而不是自己定义)
H0 = 67                # km/s/Mpc
c = 3 * 10**8          # m/s
G = 6.67 * 10**(-11)   # N·m**2/kg**2
Msun = 1.989 * 10**30  # kg


# def phi_minus4_PN(f_, z_, Mc_, fedd, epsilon):
    # """
    # 吸积与加速度效应引入的额外相位 (from PRD 126, 101105)
    # """
    # fedd is Eddington ratio, fedd:=dot{m}/dot{mEdd}, dot{m} is the mass acctretion rate of either BH and dot{mEdd}:=LEdd/eta, eta is radiative efficiency
    # epsilon is defined in (3) 
    # tau_s is Salpeter time, s
    # xi is a factor parameterizing the drag produced by momentum transfer from the accreted gas, set to 0 
    # 消除频率一开始的0
    # if abs(f_)<=0.0001:
        # f_ = 0.0001
    # tau_s = 4.5 * 10**7 * 365 * 86400
    # xi = 0
    # phi_minus4 = (-fedd*(8.0*xi+15)*(75.0*Mc_)/(851968.0*tau_s)) * (c**(-3)*G*Msun) + (25*Mc_/65536*3.2*10**(-11)*epsilon) * (G*c**(-4)*Msun)
    # return phi_minus4 * ( (1+z_) * np.pi*Mc_*f_ * Msun*(G * c**(-3.0)) )**(-13.0/3)


M_center = 10**8  # Msun
a = 0.4 * 3.26 * 3*10**8 * 86400 * 365 # pc -> m
cs = np.sqrt(2*G*M_center*Msun / a)  # sound speed, m/s 
def DF(f_, m1_, m2_, eta_, Mc_, z_, normolized_rho):
    """
    动力学摩擦引入的额外相位
    """
    # 消除频率一开始的0
    if abs(f_)<=0.0001:  
        f_ = 0.0001
    rho_0 = 10**(-7.0)            # kg/m^3
    rho = normolized_rho * rho_0
    f_DF = cs / (22*np.pi*(m1_+m2_))
    f_DF = f_DF * (c**2/G) / Msun        # convert to SI
    gamma_DF = -247*np.log(f_/f_DF) - 39 + 304*np.log(20) + 38*np.log(3125.0/8)
    DF_geo = -rho * (25*np.pi*(3*eta_-1)*Mc_**2) / (739328.0*eta_**2) * gamma_DF * (np.pi*f_*Mc_*(1+z_))**(-16.0/3)
    DF_SI = DF_geo * (G**(-7.0/3)*c**10)
    DF_SI = DF_SI * Msun**(-10.0/3)
    return DF_SI


def TaylorF2PlusEnvironmentFrequencyDomainPlusCross(fedd=5, epsilon=3.2*10**6, normolized_rho=1, **params):
    """
    输入delta_f, distance
    """
    mass1 = params["mass1"]
    mass2 = params["mass2"]
    distance = params["distance"]
    params["approximant"] = "TaylorF2"  # 基于该波形

    # redshift
    z = 10**3 * H0 * distance / c

    # chirp mass
    M = mass1 + mass2
    eta = mass1 * mass2 / (M ** 2)
    Mc = (1 + z) * (eta ** 0.6) * M

    hp_fd_without_env, hc_fd_without_env = get_fd_waveform(**params)
    
    # print("params in TaylorF2Plus = {}".format(params))
    print("len(TaylorF2PlusEnvironment) = {}".format(len(hp_fd_without_env)))  # 有450271个，使得下面的计算太慢了(来自于最内稳定轨道的f/delta_f，但是不知道为什么deltaf变小了很多，成为了1/256)

    # 先计算所有的额外相位(检验两个频率序列的sample_frequencies是否相同:相同)
    # env_phase = []
    # for i in range(len(hp_fd_without_env)):
        # if i % 1000 == 0:
            # print(i)
        # hp_fd_without_env[i] = hp_fd_without_env[i] * (np.exp(complex(0, DF(hp_fd_without_env.sample_frequencies[i], mass1, mass2, eta, Mc, z, normolized_rho) + phi_minus4_PN(hp_fd_without_env.sample_frequencies[i], z, Mc, fedd, epsilon))))
        # hc_fd_without_env[i] = hc_fd_without_env[i] * (np.exp(complex(0, DF(hp_fd_without_env.sample_frequencies[i], mass1, mass2, eta, Mc, z, normolized_rho) + phi_minus4_PN(hp_fd_without_env.sample_frequencies[i], z, Mc, fedd, epsilon))))
    # print("my wave 3")

    ##########################################################################################################################################
    # 将环境效应的函数放在主函数里面
    tau_s = 4.5 * 10**7 * 365 * 86400
    xi = 0
    M_center = 10**8  # Msun
    a = 0.4 * 3.26 * 3*10**8 * 86400 * 365 # pc -> m
    cs = np.sqrt(2*G*M_center*Msun / a)  # sound speed, m/s 
    rho_0 = 10**(-7.0)            # kg/m^3
    rho = normolized_rho * rho_0
    f_DF = cs / (22*np.pi*(mass1+mass2))
    f_DF = f_DF * (c**2/G) / Msun        # convert to SI
    frequencies_ = hp_fd_without_env.sample_frequencies
    for i in range(len(hp_fd_without_env)):
        if abs(frequencies_[i])<=0.0001:
            frequencies_[i] = 0.0001
        phi_minus4 = (-fedd*(8.0*xi+15)*(75.0*Mc)/(851968.0*tau_s)) * (c**(-3)*G*Msun) + (25*Mc/65536*3.2*10**(-11)*epsilon) * (G*c**(-4)*Msun)
        phi_minus4 = phi_minus4 * ( (1+z) * np.pi*Mc*frequencies_[i] * Msun*(G * c**(-3.0)) )**(-13.0/3)
        gamma_DF = -247*np.log(frequencies_[i]/f_DF) - 39 + 304*np.log(20) + 38*np.log(3125.0/8)
        DF_geo = -rho * (25*np.pi*(3*eta-1)*Mc**2) / (739328.0*eta**2) * gamma_DF * (np.pi*frequencies_[i]*Mc*(1+z))**(-16.0/3)
        DF_SI = DF_geo * (G**(-7.0/3)*c**10)
        DF_SI = DF_SI * Msun**(-10.0/3)
        hp_fd_without_env[i] = hp_fd_without_env[i] * (np.exp(complex(0, DF_SI + phi_minus4)))
        hc_fd_without_env[i] = hc_fd_without_env[i] * (np.exp(complex(0, DF_SI + phi_minus4)))
    ##########################################################################################################################################


    # def old2:
        # 先计算所有的额外相位(检验两个频率序列的sample_frequencies是否相同:相同)
        # env_phase = []
        # for i in range(len(hp_fd_without_env)):
            # print(i)
            # env_phase.append(np.exp(complex(0, DF(hp_fd_without_env.sample_frequencies[i], mass1, mass2, eta, Mc, z, normolized_rho) + phi_minus4_PN(hp_fd_without_env.sample_frequencies[i], z, Mc, fedd, epsilon))))
        # 
        # print("my wave 3")
        # 乘
        # for i in range(len(hp_fd_without_env)):
            # hp_fd_without_env[i] = hp_fd_without_env[i] * env_phase[i]
            # hc_fd_without_env[i] = hc_fd_without_env[i] * env_phase[i]
        # 
        # print("my wave 4")



    # def old1:
        # hp_fd = hp_fd_without_env
        # hc_fd = hc_fd_without_env

        # h_ = []
        # for i in range(len(hp_fd_without_env)):
            # h_.append(hp_fd_without_env[i])
        # for i in range(len(hp_fd_without_env)):
            # h_[i] = h_[i] * np.exp(complex(0, DF(hp_fd_without_env.sample_frequencies[i], mass1, mass2, eta, Mc, z, normolized_rho) + phi_minus4_PN(hp_fd_without_env.sample_frequencies[i], z, Mc, fedd, epsilon)))
        # hp_fd = FrequencySeries(h_, delta_f=hp_fd_without_env.delta_f, epoch=hp_fd_without_env.epoch)

        # h_ = []
        # for i in range(len(hc_fd_without_env)):
            # h_.append(hc_fd_without_env[i])
        # for i in range(len(hc_fd_without_env)):
            # h_[i] = h_[i] * np.exp(complex(0, DF(hc_fd_without_env.sample_frequencies[i], mass1, mass2, eta, Mc, z, normolized_rho) + phi_minus4_PN(hc_fd_without_env.sample_frequencies[i], z, Mc, fedd, epsilon)))
        # hc_fd = FrequencySeries(h_, delta_f=hc_fd_without_env.delta_f, epoch=hc_fd_without_env.epoch)

    return hp_fd_without_env, hc_fd_without_env


def Taylor_duration(**params):
    # More accurate duration (within LISA frequency band) of the waveform,
    # including merge, ringdown, and aligned spin effects.
    # This is used in the time-domain signal injection in PyCBC.
    import warnings
    from pycbc.waveform.spa_tmplt import spa_length_in_time
    phase_order = -1
    nparams = {'mass1':params['mass1'], 'mass2':params['mass2'], 'f_lower':params['f_lower'], 'phase_order':phase_order}
    time_length = np.float64(spa_length_in_time(**nparams))
    # print("time_length = {}".format(time_length))
    return time_length
