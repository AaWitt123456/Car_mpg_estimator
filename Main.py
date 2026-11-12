
from PredictMpg import train_model
from Interface import launch_interface


def main():
    #Starts PredictMpg
    model = train_model()

    # Launch the GUI in Interface
    launch_interface(model)


if __name__ == "__main__":
    main()

