#TODO: add date functionality with payment dates and maturities
#after this, cash flows can be generated with their applicable discount factors
#will also have to look into daycount function as this is crucial to truly
#replicating bond calculators and accurately generating principal+interest per
#period.

################################################################################

class MBS:
    #MBS class with information regarding collateral face value and coupon


    def __init__(self, collat_face_val, collat_coupon):
        '''
        init function for base MBS class
        float collat_face_val: notional amount of underlying collateral
        float collat_coupon: coupon rate (expressed as decimal) of collateral
        '''
        self._face_value = collat_face_val
        self._coupon = collat_coupon

    #generic getters
    #would like to keep class variables as private as possible here
    def get_face_val(self) -> float:
        return self._face_value

    def get_coupon(self) -> float:
        return self._coupon

    #generic setter
    #access to variables gated behind class functions
    def set_face_val(self, val) -> None:
        self._face_value = val

    def set_coupon(self, coupon) -> None:
        self._coupon = coupon

    #TODO: add some utility functions for analysis of base class.
    #not much to do here at the moment, but can work on adding pricing mechanics
    #as well as more variables


class IO(MBS):

    #IO tranche, needs some refinement
    def __init__(self, collat_face_val, collat_coupon, target_coupon):
        '''
        Interest Only tranche class based on generic MBS. Sizing tbd
        float collat_face_val: notional amount of underlying collateral
        float collat_coupon: coupon rate (expressed as decimal) of collateral
        float target_coupon: target coupon rate for IO tranche - helps
                             determine sizing of tranche

        '''
        super().__init__(collat_face_val, collat_coupon)
        self._target_coupon = target_coupon

    #generic getters
    #would like to keep class variables as private as possible here
    def get_target_coupon(self) -> float:
        return self._target_coupon


    #generic setters
    #access to variables gated behind class functions
    def set_target_coupon(self, coupon) -> None:
        self._target_coupon = coupon


class Floater(MBS):

    #floating rate tranche derived from MBS base class
    def __init__(self, collat_face_val, collat_coupon, spread, cap):
        '''
        Floating rate tranche based on generic MBS.
        float collat_face_val: notional amount of underlying collateral
        float collat_coupon: coupon rate (expressed as decimal) of collateral
        float spread: spread to benchmark (expressed as decmial)
        float cap: cap rate of floater
        '''
        super().__init__(collat_face_val, collat_coupon)
        self._spread = spread
        self._cap = cap


    #generic getters
    #would like to keep class variables as private as possible here
    def get_spread(self) -> float:
        return self._spread

    def get_cap(self) -> float:
        return self._cap


    #generic setters
    #access to variables gated behind class functions
    def set_spread(self, spread) -> None:
        self._spread = spread

    def set_cap(self, cap) -> None:
        self._cap = cap


    #utility functions
    def floater_face(self) -> float:
        '''
        Function to generate floating rate tranche face value based on interest
        available to tranche and cap rate.
        '''

        available_interest = self.get_face_val() * self.get_coupon()
        return available_interest / self.get_cap()


class InverseFloater(Floater):

    #Inverse floater
    def __init__(self, collat_face_val, collat_coupon, spread, cap):
        '''
        Inverse Floating rate tranche based on generic MBS.
        float collat_face_val: notional amount of underlying collateral
        float collat_coupon: coupon rate (expressed as decimal) of collateral
        float spread: spread to benchmark for floating rate tranche
                      (expressed as decmial)
        float cap: cap rate of floating rate tranche
        '''

        super().__init__(collat_face_val, collat_coupon, spread, cap)
        self._leverage = self.calc_leverage()
        self._cap = self.calc_cap()

    def calc_leverage(self) -> float:
        '''
        calculates inverse floater leverage to benchmark movement
        '''

        coupon = self.get_coupon()
        return coupon / (self.get_cap() / coupon)

    def calc_cap(self) -> float:
        '''
        calculates inverse floater max interest rate based on floater info

        '''

        #initializing all values ones so they do not get called multiple time
        #TODO: check if this is actually faster or if calling direct better
        collat_val = self.get_face_val()
        collat_coup = self.get_coupon()
        floater_cap = self.get_cap()
        floater_floor = self.get_spread()

        #whole-tranche cash flow
        total_flow = collat_val * collat_coup
        floater_face =  total_flow / floater_cap

        #inverse is residual of floater
        inverse_face = collat_val - floater_face
        min_floater_pay = floater_face * floater_floor
        max_inverse_pay = total_flow - min_floater_pay
        return max_inverse_pay / inverse_face
