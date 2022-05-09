
class MBS:

    def __init__(self, collat_face_val, collat_coupon):
        self._face_value = collat_face_val
        self._coupon = collat_coupon

    def get_face_val(self):
        return self._face_value

    def get_coupon(self):
        return self._coupon

    def set_face_val(self, val):
        self._face_value = val

    def set_coupon(self, coupon):
        self._coupon = coupon


class IO(MBS):

    def __init__(self, collat_face_val, collat_coupon, target_coupon):
        super().__init__(collat_face_val, collat_coupon)
        self._target_coupon = target_coupon

    def get_target_coupon(self):
        return self._target_coupon

    def set_target_coupon(self, coupon):
        self._target_coupon = coupon


class Floater(MBS):

    def __init__(self, collat_face_val, collat_coupon, spread, cap):
        super().__init__(collat_face_val, collat_coupon)
        self._spread = spread
        self._cap = cap

    def get_spread(self):
        return self._spread

    def get_cap(self):
        return self._cap

    def set_spread(self, spread):
        self._spread = spread

    def set_cap(self, cap):
        self._cap = cap

    def floater_face(self):
        available_interest = self.get_face_val() * self.get_coupon()
        return available_interest / self.get_cap()


class InverseFloater(Floater):
    def __init__(self, collat_face_val, collat_coupon, spread, cap):
        super().__init__(collat_face_val, collat_coupon, spread, cap)
        self._leverage = self.calc_leverage()
        self._cap = self.calc_cap()

    def calc_leverage(self):
        coupon = self.get_coupon()
        return coupon / (self.get_cap() / coupon)

    def calc_cap(self):
        collat_val = self.get_face_val()
        collat_coup = self.get_coupon()
        floater_cap = self.get_cap()
        floater_floor = self.get_spread()
        total_flow = collat_val * collat_coup
        floater_face =  total_flow / floater_cap
        inverse_face = collat_val - floater_face
        min_floater_pay = floater_face * floater_floor
        max_inverse_pay = total_flow - min_floater_pay
        return max_inverse_pay / inverse_face

