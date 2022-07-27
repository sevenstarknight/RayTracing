import click 

# ======================================================================================
# Local imports
from src.endtoenddemonstration import EndToEndDemo
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod

from src.logger.simlogger import get_logger, setup_applevel_logger, setup_applevel_logger

@click.command()
@click.option('--demo', is_flag=True, show_default=True, default=True, help = 'Do you want the Demo')

def main(demo):

    setup_applevel_logger(file_name="app.log")
    LOGGER = get_logger(__name__)

    if(demo):
        end2EndDemo = EndToEndDemo()

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        transIonosphereEffects = end2EndDemo.execute_XYZ(quantizationParameter)
        LOGGER.info("Total Delay: " + str(transIonosphereEffects.totalIonoDelay_sec))
        LOGGER.info("Total dB Loss: " + str(transIonosphereEffects.totalIonoLoss_db))
    else:
        LOGGER.info("Non-Demo Case Not Avalible at this time, try running the dash app instead")

if __name__ == "__main__":
    main()