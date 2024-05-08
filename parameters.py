class param:
    img_num = 10
    img_sub_num = 5000
    img_sub_num_test = 1200
    classify_decision = 1
    weight_img_track = True
    track_interval = 100
    # Neuron
    n = 50
    # (positive)
    fth = 75  # 1~255
    f = 8
    f_base = 0.0001
    # (negative)
    pixel_negative_train = -25
    pixel_negative_classify = -25
    f_negative = 15
    f_base_negative = 0.0001
    negative_start = 1
    # threshold
    Pth =  300
    Pth_max = 500
    Pth_min = 100
    # Homeostasis
    homeostasis = False
    Asymmetric_Gamma = False
    activity_range = 100
    Gamma = 0.5
    Gamma_high = 0
    Gamma_low = 0
    # Homeostasis Weight
    homeostasis_weight = False
    A_plus_percentage = 20
    A_minus_percentage = 360
    Gamma_HW = 0
    Ap_max = 50
    Ap_min = 0
    Am_max = 500
    Am_min = 0
    # STDP
    tau_plus = 2.5
    tau_minus = 3.1
    T_training = 60
    T_test = T_training
    t_back = -6
    t_fore = 3
    # weight
    w_max_initial = 2 
    w_min_initial = -1.2
    w_max = 2.99E-4
    w_min = 2.17E-5
    scale = (w_max-w_min)/(w_max_initial-w_min_initial)
    pixel_x = 28
    m = pixel_x*pixel_x 
    Pref = 1*scale 
    Prest = 1*scale
    Pmin = 1*scale 
    # D_rate = 1.6
    D = 1*scale
    no_signal_D = 0.1
    sigma = 1
    A_plus = A_plus_percentage*w_max/100
    A_minus = A_minus_percentage*w_min/100
    epoch = 1
    epochimg = 10
    Weight_x = 10
    Weight_y = int(n/Weight_x)+1 
    fr_bits = 12
    int_bits = 12
