from kedro.framework.hooks import hook_impl


class PanderaHook():
    @hook_impl
    def before_dataset_loaded(self):
        print("*** Pandera Hook - before dataset loaded ***")

    @hook_impl
    def after_dataset_loaded(self):
        print("*** Pandera Hook - after dataset loaded***")






pandera_hook = PanderaHook()