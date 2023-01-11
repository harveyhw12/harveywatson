#define ALIGN 4

#include "kernel/types.h"
#include "kernel/fcntl.h"
#include "user/user.h"

struct page {
  struct page *next;
  struct page *previous;
  uint size;
};

void _free(void *ap);
void* _malloc(uint nbytes);
void remove_node(struct page* page_to_remove);
void add_node(struct page* page_to_add);
void merge();
void more_memory(uint size);
void print_list();
