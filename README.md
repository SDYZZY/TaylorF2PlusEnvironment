# TaylorF2PlusEnvironment

## 定义

这个波形的思路是直接对TaylorF2生成的波形乘以环境效应的指数项（有时间需要画图作差验证TaylorF2和我定义的波形差异如何：较小）

时域空间的真空引力波应变为
$$
h(t) = h_{+}(t)F_{+} + h_{\times}(t)F_{\times}
$$
作傅里叶变换转换到频域空间的真空引力波波形为
$$
\tilde{h}(f)=\int_{-\infty}^{+\infty}h(t)e^{i2\pi ft}dt
$$
由于我们假设天线函数和时间无关，因此对$h(t)$作变换时，天线函数可以直接从积分里面拿出来，也就是说
$$
\begin{aligned}
\tilde{h}(f) &= \int_{-\infty}^{+\infty}[h_{+}(t)F_{+} + h_{\times}(t)F_{\times}]e^{i2\pi ft}dt \\
             &=\tilde{h}_{+}(f)F_{+} + \tilde{h}_{\times}(f)F_{\times}
\end{aligned}
$$
其中$\tilde{h}_{+,\times}(f) = \int_{-\infty}^{+\infty}h_{+,\times}(t)e^{i2\pi ft}dt$。

考虑环境效应后的频域引力波波形为
$$
\tilde{h'}(f) = \tilde{h}(f) \times e^{i(\tilde{\phi}_{DF}+\tilde{\phi}_{-4})} = \tilde{h}(f)\times e^{i\Phi_{env}}
$$
动力学摩擦的效应对应于\(-5.5\)PN
$$
\begin{align}
    \tilde{\phi}_{DF} \simeq -\rho \frac{25\pi(3\eta-1)M_{c}^{2}}{739328\eta^{2}}\gamma_{DF}[\pi M_{c}f(1+z)]^{-16/3} \text{，}
\end{align}
$$
其中$\rho$是气体密度，$\gamma_{DF}\equiv-247\ln{(f/f_{DF})}-39+304\ln{(20)}+38\ln{(3125/8)}$，$f_{DF}\equiv c_{s}/[22\pi(m_{1}+m_{2})]$。

吸积和加速度的效应对应于\(-4\)PN
$$
\begin{align}
    \tilde{\phi}_{-4} = \phi_{-4}[\pi M_{c}f(1+z)]^{-13/3} \text{。}
\end{align}
$$

其中$\phi_{-4}$是一个描述吸积和加速度的总体效应的参数.

可以将考虑环境效应后的频域引力波波形改写为
$$
\begin{align}
\tilde{h'}(f) &= [\tilde{h}_{+}(f)F_{+} + \tilde{h}_{\times}(f)F_{\times}] \times e^{i\Phi_{env}} \\
              &= \tilde{h}_{+}(f) \times e^{i\Phi_{env}} F_{+} + \tilde{h}_{\times}(f) \times e^{i\Phi_{env}} F_{\times} \\
              &= \tilde{h'}_{+}(f)F_{+} + \tilde{h'}_{\times}(f)F_{\times} 
\end{align}
$$
其中$\tilde{h'}_{+,\times}$是有环境效应的频域极化波形。也就是说，在真空中的频域波形乘上环境效应的e指数就可以得到考虑环境后的频域波形。

对上式作傅里叶反变换，得到时域中的考虑环境效应的波形为
$$
\begin{align}
h'(t) &= h'_{+}(t)F_{+} + h'_{\times}(t)F_{\times} 
\end{align}
$$
其中$h'_{+,\times}(t)$是有环境效应的时域极化波形。



## 验证：

真空中的引力波波形为$\tilde{h}(f)$，考虑环境效应后的频域波形为
$$
\tilde{h'}(f) = \tilde{h}(f) \times e^{i(\tilde{\phi}_{DF}+\tilde{\phi}_{-4})} = \tilde{h}(f)\times e^{i\Phi_{env}}
$$
它们的差异为
$$
\begin{align}
\tilde{h}(f) - \tilde{h'}(f) &= \tilde{h}(f)[1-\exp(i\Phi_{env})] \\
 &= \tilde{h}(f)[1-\exp(\tilde{\phi}_{DF}+\tilde{\phi}_{-4})]
\end{align}
$$
































