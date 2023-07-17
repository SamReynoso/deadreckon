import config
from mock_data.mock import Mock
from cli import cli
from plotter import plotter
from deadreckon.gps import GPS


def main():
        cli.clear()
        origin, destination, craft_speed, limit, selection = cli.run()
        suc = False
        if selection == "r":
            cli.clear()
            gps = GPS(origin, destination, craft_speed)
            for i in range(limit):
                cli.readout.status(i)
                gps.main()
                gps.save_csv()
                plotter(gps)
                if gps.deadreckon.vectors.target.mag < config.WITHIN_TARGET:
                    suc = True
                    if config.STOP_AT_COMPLETION:
                        break
                MOCK.next()
                cli.clear()
        if suc:
            cli.success()
        cli.clear()


if __name__ == "__main__":
    MOCK = Mock()
    MOCK.set_defaults()
    main()