__all__ = ['Meter']
from decimal import Decimal

from .FormControl import FormControl

class Meter(FormControl):
    width = 100
    toblue = False
    """ The silly little meter. yay """
        
    def draw(self):
        value = self.value or self.name
        return """
        <table border='0' cellspacing='0' cellpadding='0' width='%s' 
            style='border: 0px;'>
        <tr>
            <td style='border: 0px;'>
                <div style='
                    border: 1px solid; 
                    width: %s;
                    height: 12px;
                    background-color: #%s;'></td>
            <td style='font-size: .8em;
                border: 0px;
                width: 50;
                text-align: right;'>
                %s%%
            </td>
        </tr>
        </table>
        """ % (
            self.width + 50,
            self.value,
            self.meterLevel(),
            self.value
        )

    def meterLevel(self):
        """ Returns red through yellow to green
            0 ff0000
           10 ff3300
           20 ff6600
           30 ff9900
           40 ffcc00
           50 ffff00
           60 ccff00
           70 99ff00
           80 66ff00
           90 33ff00
          100 00ff00
        """
        value = Decimal(self.value)
        if self.toblue:
            if value < 10:
                return 'FF00%02d' % value
            elif value < 50:
                return 'FF00%X' % int(Decimal(str(value))*Decimal('5.1'))
            elif value == Decimal(50):
                return 'ff00ff'
            else:
                v = (100 - Decimal(str(value)))*Decimal('5.1')
                if v < 10:
                    return '%02d00FF' % int(v)
                else: 
                    return '%X00FF' % int(v)

        else:
            if value < 10:
                return 'FF%02d00' % value
            elif value < 50:
                return 'FF%X00' % int(Decimal(str(value))*Decimal('5.1'))
            elif value == Decimal(50):
                return 'ffff00'
            else:
                v = (100 - Decimal(str(value)))*Decimal('5.1')
                if v < 10:
                    return '%02dFF00' % int(v)
                else: 
                    return '%XFF00' % int(v)

