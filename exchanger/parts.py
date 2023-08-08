class Part:
    def __init__(self, heat_transferability: float = None, heat_transfer_area: float = None,
                 heat_transfer_coefficient: float = None):

        if heat_transferability is None:
            if heat_transfer_area is None and heat_transfer_coefficient is None:
                self.heat_transferability = 0.0
            else:
                self.heat_transfer_area = heat_transfer_area
                self.heat_transfer_coefficient = heat_transfer_coefficient
        else:
            self.heat_transferability = heat_transferability
        # @TODO implement more init parameters

    @property
    def heat_transfer_area(self):
        try:
            value = self._heat_transfer_area
        except AttributeError:
            value = None
        finally:
            return value

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        if self.heat_transferability is None:
            self._heat_transfer_area = value
        else:
            raise AttributeError("heat_transferability already set")

    def heat_transfer_area_str(self) -> str:
        try:
            return f"heat transfer area:%.4f mm^2\n" % self.heat_transfer_area
        except TypeError:
            return ""

    @property
    def heat_transfer_coefficient(self):
        try:
            value = self._heat_transfer_coefficient
        except AttributeError:
            value = None
        finally:
            return value

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        if self.heat_transferability is None:
            self._heat_transfer_coefficient = value
        else:
            raise AttributeError("heat_transferability aleready set")

    def heat_transfer_coefficient_str(self) -> str:
        try:
            return f"heat transfer coefficient: %.2f W/(m^2 K)\n" % (self.heat_transfer_coefficient)
        except TypeError:
            return ""

    @property
    def heat_transferability(self):
        try:
            value = self._heat_transferability
        except AttributeError:
            try:
                value = self.heat_transfer_area * self.heat_transfer_coefficient
            except TypeError:
                value = None
        return value

    @heat_transferability.setter
    def heat_transferability(self, value):
        # @TODO better handling requiered
        try:
            del self._heat_transfer_area
            del self._heat_transfer_coefficient
        except AttributeError:
            pass
        self._heat_transferability = value

    def heat_transferability_str(self):
        return f"heat transferability: {self.heat_transferability:.3f} W/K\n"

    @property
    def hydraulic_diameter(self):
        try:
            value = self._hydraulic_diameter
        except AttributeError:
            value = None
        finally:
            return value

    @hydraulic_diameter.setter
    def hydraulic_diameter(self, value):
        self._hydraulic_diameter = value

    def hydraulic_diameter_str(self) -> str:
        try:
            return f"hydraulic diameter = %.4f mm\n" % (self.hydraulic_diameter * 1e-3)
        except TypeError:
            return ""

    def __repr__(self):
        output = f"part:\n" \
                 f"\t id = {id(self)}\n" \
                 f"\t typ: {self.__class__.__name__}\n"
        output += f"hydraulic properties:\n" + self.hydraulic_diameter_str()
        output += f"\nThermische Eigenschaften:\n" + \
                  self.heat_transferability_str() + \
                  self.heat_transfer_area_str() + \
                  self.heat_transfer_coefficient_str()

        return output
