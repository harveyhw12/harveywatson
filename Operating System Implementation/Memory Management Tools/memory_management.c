#include "memory_management.h"

struct page firstnode;
struct page *header_pointer = 0;


void _free(void *ap) {

  struct page* page_to_free = (struct page*)(unsigned long)(ap - sizeof(struct page));

  if (page_to_free > 0) {
    add_node(page_to_free);
    merge();

    struct page* current = header_pointer;
    do {
      if (current->next == current) {
        break;
      } else if (current->next != 0) {
        current = current->next;
      }
    } while (current->next != 0);
    if(current->size >= 4096) {
      if(current->size > 4096) {
        int multiple = current->size / 4096;
        int to_subtract = 4096 * multiple;
        current->size = current->size - to_subtract;
        sbrk(-to_subtract);
      } else if (current->size == 4096) {
        remove_node(current);
        sbrk(-4096);
      }
    }
  } else {
  }
};

void* _malloc(uint nbytes) {
  uint size = nbytes;
  if (size <= 0) {
    return 0;
  }
  if (size % ALIGN != 0) {
    int remainder = size % ALIGN;
    size = size + (ALIGN-remainder);
  }
  if(header_pointer == 0) {
    struct page* new_space = (struct page*)sbrk(4096 * ALIGN);
    new_space->size = 4096*ALIGN;
    new_space->next = 0;
    new_space->previous = 0;
    header_pointer = new_space;
  }
  struct page* current = header_pointer;
  do {
    if(current->size >= size) {
      if(current->size > size) {
        struct page* new = (struct page*)((unsigned long)current + sizeof(struct page)+size);
        new->size = current->size - size;
        new->next = current->next;
        new->previous = current;
        current->next = new;
        add_node(new);
        header_pointer = new;
        current->size = size;
        if(current->next == 0) {
          current->previous->next = 0;
        } else if (current->previous == 0) {
           current->next->previous = 0;
           header_pointer = current->previous;
        } else {
          current->previous->next = current->next;
          current->next->previous = current->previous;
        }
        void* to_return = (void*)((unsigned long)(current)+sizeof(struct page));
        header_pointer = current->next;
        return to_return;
      } else if(current->size == size) {
        struct page* to_return = (struct page*)((unsigned long)(current + sizeof(struct page)));
        if(current->next == 0) {
          current->previous->next = 0;
        } else if (current->previous == 0) {
           current->next->previous = 0;
           header_pointer = current->previous;
        } else {
          current->previous->next = current->next;
          current->next->previous = current->previous;
        }
        return (void*)(to_return);
      }
    }
    current = current->next;
  }while(current->next != 0);
  more_memory(size);
  void* to_return = _malloc(size);
  return to_return;
};


void remove_node(struct page* page_to_remove) {
      if(page_to_remove->next == 0) {
        page_to_remove->previous->next = 0;
      } else {
        page_to_remove->previous->next = page_to_remove->next;
        page_to_remove->next->previous = page_to_remove->previous;
      }
};


void add_node(struct page* page_to_add) {
  page_to_add->previous = 0;
  page_to_add->next = 0;
  if(page_to_add < header_pointer) {
    page_to_add->previous = 0;
    page_to_add->next = header_pointer;
    header_pointer->previous = page_to_add;
    header_pointer = page_to_add;
    return;
  }
  struct page* current = header_pointer;
  for(; current->next == 0;current = current->next) {
    if(current < page_to_add && current->next > page_to_add){
      page_to_add->next = current->next;
      page_to_add->previous = current;
      current->next = page_to_add;
      current->next->previous = page_to_add;
      return;
    }
  }
  if(page_to_add > current) {
    page_to_add->next = 0;
    page_to_add->previous = current;
    current->next = page_to_add;
    return;
  }

};

void merge() {

  struct page* current = header_pointer;
  do {
    if((unsigned long)current + (unsigned long)current->size + (unsigned long)(sizeof(struct page)) == (unsigned long)current->next) {
      current->size = (unsigned long)current->size + (unsigned long)current->next->size + sizeof(struct page);
      current->next = current->next->next;
      current->next->previous = current;
      merge();
    }
    if(current->next == current){
      return;
    } else if((unsigned long)current->next == (unsigned long)0){
      return;
    } else if (current->next != current) {
      current = current->next;
    }
  }while(current->next != current);
};


void more_memory(uint size) {
  if (size < 4096) {
    size = 4096;
  }
  char* p = sbrk(size * ALIGN);
  struct page* new_memory = (struct page*)p;
  new_memory->size = size * ALIGN;
  new_memory->next = 0;
  new_memory->previous = 0;
  //printf("enters add_node here\n");
  add_node(new_memory);
};

void print_list() {
  struct page* current = header_pointer;
  for(;current->next == 0 || current->next == current; current = current->next){
    printf("current: %d, current size: %d, current->next: %d\n", (unsigned long)current, (unsigned long)current->size, (unsigned long)current->next);

  };
}
