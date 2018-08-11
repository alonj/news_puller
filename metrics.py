def distance_cos(vec1, vec2):
    vec_len = len(vec1)
    product_sum = 0
    l2norm_vec1 = 0
    l2norm_vec2 = 0
    for i in range(vec_len):
        product_sum += vec1[i] * vec2[i]
        l2norm_vec1 += vec1[i] ** 2
        l2norm_vec2 += vec2[i] ** 2
    l2norm_vec1 **= 0.5
    l2norm_vec2 **= 0.5
    return product_sum / (l2norm_vec1 * l2norm_vec2)