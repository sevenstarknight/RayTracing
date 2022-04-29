import click 

# ======================================================================================
# Local imports
from src.endtoenddemonstration import EndToEndDemo

print("This is my file to the raytracer.")
@click.command()
@click.option('--demo', is_flag=True, show_default=True, default=True, help = 'Do you want the Demo')

def main(demo):

    if(demo):
        end2EndDemo = EndToEndDemo()
        transIonosphereEffects = end2EndDemo.execute()
        print("Total Delay: " + transIonosphereEffects.totalIonoDelay_sec)
        print("Total dB Loss: " + transIonosphereEffects.totalIonoLoss_db)
    else:
        print("Non-Demo Case Not Avalible at this time, try running the dash app instead")

if __name__ == "__main__":
    main()