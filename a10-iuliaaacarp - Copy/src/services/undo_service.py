class FunctionCall:
    def __init__(self, function_name, *function_params):
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        self._function_name(*self._function_params)

class Operation:
    def __init__(self, func_undo: FunctionCall, func_redo: FunctionCall):
        self._func_undo = func_undo
        self._func_redo = func_redo

    def undo(self):
        self._func_undo.call()

    def redo(self):
        self._func_redo.call()

class UndoRedoException(Exception):
    pass

class NoOperationsToUndo(UndoRedoException):
    pass

class NoOperationsToRedo(UndoRedoException):
    pass

class CascadedOperation:
    """
    Groups multiple Operation objects into a single undoable/redoable unit.
    """
    def __init__(self, *operations):
        self._operations = operations

    def undo(self):
        """
        Executes the undo action for all contained operations in REVERSE order.
        """
        for op in reversed(self._operations):
            op.undo()

    def redo(self):
        """
        Executes the redo action for all contained operations in FORWARD order.
        """
        for op in self._operations:
            op.redo()

class UndoService:
    def __init__(self):
        self.__history = []
        self.__index = 0

    def undo(self):
        """
        Reverts the last recorded operation.
        """
        if self.__index == 0:
            raise NoOperationsToUndo("No operations to undo.")
        self.__index -= 1
        operation = self.__history[self.__index]
        operation.undo()

    def redo(self):
        """
        Re-performs the last undone operation.
        """
        if self.__index == len(self.__history):
            raise NoOperationsToRedo("No operations to redo.")
        operation = self.__history[self.__index]
        operation.redo()
        self.__index += 1

    def record(self, operation):
        """
        Records a new operation, discarding any operations that were in the redo stack.
        :param operation: An Operation or CascadedOperation object.
        """
        self.__history = self.__history[:self.__index]
        self.__history.append(operation)
        self.__index = len(self.__history)

